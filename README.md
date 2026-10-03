# Google Sign-In for Unity

[![OpenUPM: pending](https://img.shields.io/badge/OpenUPM-pending-yellow)](Packages/com.coolishbee.google-signin/README.md#installation-via-git)
[![CI](https://github.com/coolishbee/google-signin-unity/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/coolishbee/google-signin-unity/actions/workflows/release.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue)](Packages/com.coolishbee.google-signin/LICENSE)

A Google Sign-In package for Android, iOS, the Unity Editor, and desktop players.

## Repository layout

The repository root is not a Unity project.

| Path | Purpose |
|---|---|
| [Packages/com.coolishbee.google-signin/](Packages/com.coolishbee.google-signin/) | Distributable UPM package |
| [SampleProject/](SampleProject/) | Sample Unity project referencing the local package |

## Getting started

See the [package README](Packages/com.coolishbee.google-signin/README.md) for installation, configuration, usage examples, and platform limitations.

To try the package locally, open `SampleProject/` in Unity `6000.3.18f1`. The sample is already included in that project.

## Source and license

This project is a fork of [Google's original repository](https://github.com/googlesamples/google-signin-unity). Its implementation was adapted and reworked for this project's goals using [Thaina/google-signin-unity](https://github.com/Thaina/google-signin-unity) as a reference.

Existing copyright notices are preserved. See [LICENSE](Packages/com.coolishbee.google-signin/LICENSE) for the Apache License 2.0 text.
