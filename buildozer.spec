[app]
title = BankApp
package.name = bankapp
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,jpg,txt
version = 0.1
orientation = portrait
fullscreen = 0
entrypoint = bank_projectt.py

requirements = python3, kivy

icon.filename = icon.png

android.minapi = 21
android.sdk = 34
android.ndk = 25b
android.archs = armeabi-v7a, arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
