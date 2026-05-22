# Quick Start

```bash
npm install          # Install dependencies
npm start            # Start Expo dev server
```

- Scan QR code with **Expo Go** (Android/iOS)
- Or press `a` for Android emulator / `i` for iOS simulator

## Publishing (EAS Build)

```bash
eas login                         # Log in to Expo account
eas build:configure               # Generate eas.json
eas build --platform android      # Build APK/AAB
eas build --platform ios          # Build IPA (macOS only)
eas build --platform all          # Build for both
eas submit --platform android     # Submit to Play Store
eas submit --platform ios         # Submit to App Store
```

Requires an [Expo account](https://expo.dev) and EAS CLI (`npm install -g eas-cli`).

## Troubleshooting

If the app shows an old version:

```bash
npm start -- --clear   # Clear Metro bundler cache
```

Still stuck?
- **Expo Go**: Settings → Apps → Expo Go → Storage → Clear Cache
- Or uninstall & reinstall Expo Go
