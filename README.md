# ha-pushed
Home Assistant notifications via Pushed.co

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)


In configuration.yaml, set up the notification platform:
```
notify:
  - name: pushed
    platform: pushed
    app_key: !secret pushed_app_key
    app_secret: !secret pushed_app_secret
```

Test that the platform works with developer tools -> service: `notify.pushed` -> service data: `{"message": "Hello World!"}`
