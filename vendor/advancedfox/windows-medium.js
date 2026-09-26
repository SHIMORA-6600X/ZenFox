/*
 * ==========================================
 *  Name: AdvancedFox.
 *  Version: 1.1.0.
 *  Type: Release.
 *  Level: Medium.
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
user_pref("geo.provider.network.url", "");

// ------------------------------------------
// WebRTC Control
// ------------------------------------------
user_pref("media.peerconnection.enabled", false);

// ------------------------------------------
// Referer & DoH Control
// ------------------------------------------
user_pref("network.dns.disablePrefetch", true);
user_pref("network.http.referer.trimmingPolicy", 1);
user_pref("network.http.referer.XOriginTrimmingPolicy", 2);
user_pref("network.prefetch-next", false);
user_pref("network.trr.custom_uri", "https://doh.libredns.gr/dns-query");
user_pref("network.trr.default_provider_uri", "https://doh.libredns.gr/dns-query");
user_pref("network.trr.mode", 2);
user_pref("network.trr.uri", "https://doh.libredns.gr/dns-query");

// ------------------------------------------
// Resist Fingerprinting Control
// ------------------------------------------
user_pref("privacy.fingerprintingProtection", false);
user_pref("privacy.firstparty.isolate", true);
user_pref("privacy.globalprivacycontrol.enabled", true);
user_pref("privacy.globalprivacycontrol.was_ever_enabled", true);
user_pref("privacy.trackingprotection.emailtracking.enabled", true);
user_pref("privacy.trackingprotection.enabled", true);
user_pref("privacy.trackingprotection.socialtracking.enabled", true);
user_pref("privacy.resistFingerprinting", true);
user_pref("privacy.resistFingerprinting.letterboxing.didForceSize", true);
user_pref("privacy.resistFingerprinting.letterboxing.gradient", true);
user_pref("privacy.resistFingerprinting.letterboxing.rememberSize", false);
user_pref("privacy.resistFingerprinting.letterboxing.vcenter", true);
user_pref("privacy.resistFingerprinting.pbmode", true);
user_pref("privacy.resistFingerprinting.randomDataOnCanvasExtract", true);


// Note: Some websites like Discord or Google Meet can be broken, because "media.peerconnection.enabled", so you can disable it temporery via "about:config".
// If you try to locate your location via OpenStreetMap or Google Maps, you will encounter issues with this user.js because there is no location provider because the user.js was removed the Google Location Provider, so you have to edit the user.js and add a location provider in "geo.provider.network.url".
// If you are using a Screen Reader or something like that, you will face issues, so you can temporery set "accessibility.force_disabled" to 0.