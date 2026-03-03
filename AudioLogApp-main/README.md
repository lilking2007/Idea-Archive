# AudioLog Android App

This is a complete Android project for continuous background audio recording with loop recording, storage management, and modern UI.

## Features
- **Continuous Background Recording**: Runs a foreground service with notification.
- **Loop Recording**: Automatically deletes oldest non-locked recordings when storage limit is reached.
- **Modern UI**: Built with Jetpack Compose and Material 3.
- **Settings**: Configurable clip length (1-30 min), storage limit, audio quality.
- **Privacy & Legal**: Disclaimer regarding recording laws.

## Requirements
- Android Studio Hedgehog or newer (recommended).
- Android SDK focused on API 34 (Android 14).
- Minimum API level: 33 (Android 13).

## Setup Instructions
1. **Open in Android Studio**:
   - Open Android Studio.
   - Select "Open" and navigate to this folder (`AudioLogApp`).
   - Wait for Gradle sync to complete.

2. **Build and Run**:
   - Connect your Moto G35 via USB with USB Debugging enabled.
   - Click the green "Run" button (Shift+F10).
   - Grant necessary permissions (Microphone, Notification) on first launch.

3. **Build APK**:
   - Go to `Build > Build Bundle(s) / APK(s) > Build APK(s)`.
   - The APK will be located in `app/build/outputs/apk/debug/app-debug.apk`.
   - Copy this APK to your phone to install manually if needed.

## Usage
- **Start**: Tap the large Start button on Home screen.
- **Settings**: Configure clip length and storage limit before starting long sessions.
- **Recordings**: View, play, lock, or delete recordings from the list screen.
- **Background**: The app will continue recording even if you close the UI, as long as the notification is visible.

## Troubleshooting
- **Permission Denied**: If denied once, go to Android Settings > Apps > AudioLog > Permissions and allow Microphone.
- **Service Stopped**: If the system kills the service (rare on modern Android with foreground service), restart the recording manually. The app attempts to stay alive with `START_STICKY`.

## Project Structure
- `app/src/main/java/com/audiolog/app`: Kotlin source code.
  - `service/AudioRecorderService.kt`: Core recording logic.
  - `data/StorageManager.kt`: File management and loop logic.
  - `ui/screens/`: Composable UI screens.
- `app/src/main/res`: Resources (icons, strings).
