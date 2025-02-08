# CTFd/plugins/ctfd_penalty/__init__.py

import os
from flask import Blueprint, render_template, request
from CTFd.models import Awards, Challenges, db
from CTFd.utils.decorators import admins_only
from CTFd.utils.modes import get_model
from CTFd.utils.user import get_current_user, get_current_team
from CTFd.plugins.challenges import CHALLENGE_CLASSES, BaseChallenge
from CTFd.utils import get_config, set_config
from CTFd.cache import clear_standings
from CTFd.utils.plugins import override_template
from CTFd.plugins import register_plugin_assets_directory

def load(app):
    plugin_name = "ctfd_penalty"
    blueprint = Blueprint(
        plugin_name,
        __name__,
        template_folder="templates",
        static_folder="assets",
    )

    # Get plugin location
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_name = os.path.basename(dir_path)

    # Register assets
    register_plugin_assets_directory(
        app, base_path=f"/plugins/{dir_name}/assets/", endpoint="ctfd_penalty_assets"
    )

    # Override templates
    override_template('penalty_config.html', 
        open(os.path.join(dir_path, 'assets/admin/penalty_config.html')).read()
    )

    # Configuration par défaut
    if get_config("penalty_enabled") is None:
        set_config("penalty_enabled", True)
        set_config("penalty_type", "percentage")
        set_config("penalty_value", 5)

    def create_penalty(user, team, challenge, submission):
        try:
            if not get_config("penalty_enabled"):
                return

            penalty_type = get_config("penalty_type", "percentage")
            penalty_value = int(get_config("penalty_value", 5))

            if penalty_type == "percentage":
                final_penalty = -int(challenge.value * penalty_value / 100)
            else:
                final_penalty = -penalty_value

            award = Awards(
                user_id=user.id if user else None,
                team_id=team.id if team else None,
                name=f"Penalty for failed attempt on {challenge.name}",
                description=f"Penalty for wrong answer (submitted: {submission})",
                value=final_penalty,
                category="penalty"
            )
            
            db.session.add(award)
            db.session.commit()
            clear_standings()
        except Exception as e:
            print(f"Error creating penalty: {str(e)}")

    def wrap_challenge_class(challenge_class):
        class WrappedChallenge(challenge_class):
            @classmethod
            def attempt(cls, challenge, request):
                data = request.get_json() if request.is_json else request.form
                submission = data.get('submission', '').strip()

                try:
                    status, message = challenge_class.attempt(challenge, request)

                    if status is False:
                        if not request.args.get('preview'):
                            user = get_current_user()
                            team = get_current_team()
                            create_penalty(user, team, challenge, submission)

                    return status, message
                    
                except Exception as e:
                    print(f"Error in wrapped attempt: {str(e)}")
                    return False, "An error occurred while checking your submission"

        WrappedChallenge.__name__ = challenge_class.__name__
        WrappedChallenge.id = challenge_class.id
        WrappedChallenge.name = challenge_class.name
        
        return WrappedChallenge

    @blueprint.route("/admin/plugins/penalty", methods=["GET", "POST"])
    @admins_only
    def admin_penalty():
        # Charger les configurations actuelles
        enabled = bool(get_config("penalty_enabled", True))
        penalty_type = str(get_config("penalty_type", "percentage"))
        penalty_value = int(get_config("penalty_value", 5))

        return render_template(
            "penalty_config.html",
            enabled=enabled,
            penalty_type=penalty_type,
            penalty_value=penalty_value
        )

    @blueprint.route("/api/v1/penalties/settings", methods=["POST"])
    @admins_only
    def update_settings():
        data = request.get_json()
        
        try:
            enabled = data.get("enabled", True)
            penalty_type = data.get("penalty_type", "percentage")
            penalty_value = abs(int(data.get("penalty_value", 5)))

            set_config("penalty_enabled", enabled)
            set_config("penalty_type", penalty_type)
            set_config("penalty_value", penalty_value)

            return {"success": True}
        except Exception as e:
            print(f"Error saving settings: {str(e)}")
            return {"success": False, "errors": {"": str(e)}}, 400

    # Register blueprint
    app.register_blueprint(blueprint)

    # Wrap challenge classes
    for name, challenge_class in CHALLENGE_CLASSES.items():
        CHALLENGE_CLASSES[name] = wrap_challenge_class(challenge_class)

    print("CTFd Penalty plugin loaded successfully!")