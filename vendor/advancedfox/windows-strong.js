/*
 * ==========================================
 *  Name: AdvancedFox.
 *  Version: 1.1.0.
 *  Type: Release.
 *  Level: Strong.
 *  Platforms: Windows only.
 *  Created by: iAhmed_7024-Group.
 *  Date: 14 Apr 2026.
 *  Purpose: Maximum Privacy, Anti-Fingerprinting, Security
 *  License: MIT.
 * ==========================================
*/

// ------------------------------------------
// Accessibility API Control
// ------------------------------------------
user_pref("accessibility.force_disabled", 1);

// ------------------------------------------
// Enhanced Tracking Protection (custom)
// ------------------------------------------
user_pref("browser.contentblocking.category", "custom");
user_pref("browser.download.useDownloadDir", false);
user_pref("browser.search.region", "IC");
user_pref("browser.search.reset.enabled", false);
user_pref("browser.uitour.enabled", false);

// ------------------------------------------
// HTTPS Only Mode
// ------------------------------------------
user_pref("dom.security.https_only_mode", true);
user_pref("dom.security.https_only_mode_ever_enabled", true);

// ------------------------------------------
// Geo Location Control
// ------------------------------------------
user_pref("geo.enabled", false);
user_pref("geo.provider.network.url", "");

// ------------------------------------------
// WebRTC Control
// ------------------------------------------
user_pref("media.peerconnection.enabled", false);

// ------------------------------------------
// Referer & DoH Control
// ------------------------------------------
user_pref("network.dns.disablePrefetch", true);
user_pref("network.http.http2.enabled", false);
user_pref("network.http.referer.trimmingPolicy", 2);
user_pref("network.http.referer.XOriginPolicy", 2);
user_pref("network.http.referer.XOriginTrimmingPolicy", 2);
user_pref("network.prefetch-next", false);
user_pref("network.trr.custom_uri", "https://doh.libredns.gr/dns-query");
user_pref("network.trr.default_provider_uri", "https://doh.libredns.gr/dns-query");
user_pref("network.trr.mode", 3);
user_pref("network.trr.uri", "https://doh.libredns.gr/dns-query");

// ------------------------------------------
// Resist Fingerprinting Control
// ------------------------------------------
user_pref("privacy.fingerprintingProtection", false);
user_pref("privacy.firstparty.isolate", true);
user_pref("privacy.trackingprotection.emailtracking.enabled", true);
user_pref("privacy.trackingprotection.enabled", true);
user_pref("privacy.trackingprotection.socialtracking.enabled", true);
user_pref("privacy.globalprivacycontrol.enabled", true);
user_pref("privacy.globalprivacycontrol.was_ever_enabled", true);
user_pref("privacy.resistFingerprinting", true);
user_pref("privacy.resistFingerprinting.letterboxing", true);
user_pref("privacy.resistFingerprinting.letterboxing.didForceSize", true);
user_pref("privacy.resistFingerprinting.letterboxing.gradient", true);
user_pref("privacy.resistFingerprinting.letterboxing.rememberSize", false);
user_pref("privacy.resistFingerprinting.letterboxing.vcenter", true);
user_pref("privacy.resistFingerprinting.pbmode", true);
user_pref("privacy.resistFingerprinting.randomDataOnCanvasExtract", true);


// Note: Some websites like Discord or Google Meet can be broken, because "media.peerconnection.enabled", so you can disable it temporery via "about:config",
// "network.http.referer.XOriginPolicy" and "network.http.referer.trimmingPolicy" can cause some problems with some websites.
// for "network.http.referer.XOriginPolicy", you can set it to 0 if you encounter problems, and for "network.http.referer.trimmingPolicy", you can set it to 1 to balance between user experience and privacy.
// "network.http.http2.enabled" may break some websites like Google Maps or Claude AI, so you may have to enable it temporery.
// "privacy.resistFingerprinting" may break some websites like Claude AI website, the solution is by adding the website link in "privacy.resistFingerprinting.exemptedDomains", and if you want to add multiple links, seperate them with ", ".
// If you try to locate your location via OpenStreetMap or Google Maps, you will encounter issues with this user.js because there is no location provider because the user.js was removed the Google Location Provider, so you have to edit the user.js and add a location provider in "geo.provider.network.url".
// If you are using a Screen Reader or something like that, you will face issues, so you can temporery set "accessibility.force_disabled" to 0.
// You may encounter slow loading for some websites or some websites is blocked and you can't access it, these issues may because DoH, so you can exclude these websites by adding them in "network.trr.excluded-domains" in "about:config", and if you want to add multiple links, seperate them with ", ".

// If you're asking: "Why I have to edit these configurations every time?". You chose "Strong" level, if you don't want to edit every time, use "Medium" or "Weak" levels or edit the user.js itself.