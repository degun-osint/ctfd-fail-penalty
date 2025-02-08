# CTFd Penalty Plugin

A CTFd plugin that adds penalties for wrong challenge submissions. When a participant submits an incorrect flag, they receive a penalty that reduces their score.

## Features

- Configurable penalty system for wrong flag submissions
- Two penalty types:
  - Percentage: Deducts a percentage of the challenge's value
  - Fixed: Deducts a fixed number of points
- Penalties appear as negative awards in the team/user history
- Admin interface to configure penalties
- Can be enabled/disabled without removing the plugin

## Installation

1. Clone this repository into your CTFd plugins directory:
```bash
cd /path/to/CTFd/CTFd/plugins
git clone https://github.com/yourusername/ctfd-penalty.git ctfd_penalty
```

2. Make sure the plugin directory structure is as follows:
```
CTFd/plugins/ctfd_penalty/
├── README.md
├── __init__.py
├── assets/
│   └── admin/
│       ├── js/
│       │   └── penalty_settings.js
│       └── penalty_config.html
└── config.json
```

3. Restart CTFd
```bash
docker restart ctfd
```

## Configuration

1. Log in as an admin
2. Go to Admin Panel → Plugins → Challenge Penalty
3. Configure:
   - Enable/disable penalties
   - Choose penalty type (percentage or fixed points)
   - Set the penalty value (percentage or points)
4. Click "Save Settings"

## Usage

Once configured, the plugin automatically:
1. Monitors challenge submissions
2. Applies penalties for incorrect submissions based on your settings
3. Creates negative award entries in the user/team history
4. Updates the scoreboard accordingly

## Notes

- Penalties are applied immediately after an incorrect submission
- Penalties stack (multiple wrong submissions = multiple penalties)
- Penalties are visible in the awards section of the user/team pages
- Penalties affect the scoreboard in real-time
- The plugin works in both user and team modes

## Support

For issues, feature requests, or contributions, please:
1. Check existing issues
2. Open a new issue with:
   - CTFd version
   - Clear description of the problem/request
   - Steps to reproduce (if reporting a bug)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the GPL V3 License - see the LICENSE file for details

## Credits

Created by Degun