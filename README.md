## ZenFox 

<p align="center">
  <a href="https://discord.gg/bQxe2dkgMW"><img src="https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&logoColor=blue" alt="Discord"></a>
  <a href="https://t.me/shimora_projects"><img src="https://img.shields.io/badge/Telegram-Join-26A5E4?logo=telegram&logoColor=sky" alt="Join Telegram"></a>
</p>

[about:config](https://support.mozilla.org/en-US/kb/about-config-editor-firefox) tweaks for [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/new/).

_Support : Firefox 115_ +

#### Files (pick what you need)

| _File_ 📂 | _Topic_ 🪄 | _Features_ ✨ |
|------|---------|-------|
| _`ZenFox.js`_ | _Performance_ ⚡️ | _Performance-focused configuration to improve responsiveness,reduce CPU usage,and speed up browsing_ | 
| _`LiteFox.js`_ | _Debloating_ ♻️ | _Strips unnecessary features to keep Firefox clean, lightweight, and distraction-free_ |
| _`Softfox.js`_ | _Smooth Scrolling_ 🖌 | _Enhances scrolling behavior for a smoother and more fluid browsing experience_ | 
| _`policies.json`_ | __ | _Applies privacy-oriented enterprise policies, including telemetry reduction and privacy-focused search engine settings_ | 

#### 📥 _Installation_

> ⚠️ Back up your profile first. `user.js` values persist in `prefs.js` even after you delete `user.js`.

1. _Create a backup profile_ (`about:profiles > Back up` or copy the folder).

2. _Download `ZenFox.zip` from Releases_ (not the `Source code` archive). Zip contains: `ZenFox.js`, `LiteFox.js`, `Softfox.js`, `policies.json`,`LICENSE`.

3. _Review overrides_ — search for `Max opt-in` and `[REMOVED v157]` to see aggressive/legacy options.

4. _Open `about:profiles`_, click **Open Folder** on Root Directory for the target profile.

5. _Copy `user.js` (and optionally `LiteFox.js`/`Softfox.js` merged or as separate test runs) into the folder._ `policies.json` goes to Firefox install `distribution/` folder (admin), not the profile.

6. _Restart Firefox._



#### ↩️ Uninstall / Revert

Deleting `user.js` does **not** revert applied prefs. Either:
- Restore your backup profile folder, or
- `about:support > Refresh Firefox`, or
- `about:config` → reset each `user_pref` key manually.

#### ✨ _Features_

• ⚡️ _Faster Page Loads – Balanced network/rendering (pacing on, 900 connections, sane DNS cache)_

• 🛠 _Optimized Cache – 512MB disk + 512MB media defaults; repeat visits faster without 1GB bloat_

• 🔋 _Lightweight – Session restore lazy, 10 undo tabs, tab unload on low memory_

• 🔌 _Compatibility – WebRender + Canvas accel with fallback notes for old GPUs/VMs_

• 🪄 _Smooth – One active scroll profile (ZEN), 60/90/120Hz alternatives commented_

• 🛠 _De-bloated (LiteFox) – AI/chatbot/translations/sponsored stories off, Pocket remnants removed_


|*It's important to read this* |  *Files*    | _Note_    |
|-------|-----|-------|
| *Don't Download it* |  *Source code* ❎ | *that's the source code on main page not in Releases* |
|  *Download it*      |  *ZenFox.zip* ✔️| *Built by `tools/build.sh`, includes checksums*  |

#### 💎 _SUPPORT_

_If you like my project please leave a star_ ⭐ 

#### 🌹 _SPECIAL THANKS FOR_ 
[A7](https://github.com/A7md70242602GH)
_gives me some ideas & testing the project_

[Kenjaku](https://github.com/kenjaku-dev)
_helps me to make a website for my project_

#### 🧾 _LICENSE_
_This project is under_ [MIT](https://github.com/SHIMORA-6600X/NitroFox/blob/main/LICENSE) _license_
