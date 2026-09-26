/*
 * ==========================================
 *  Name: AdvancedFox.
 *  Version: 1.1.0.
 *  Type: Release.
 *  Level: Weak.
 *  Platforms: Linux only.
 *  Created by: iAhmed_7024-Group.
 *  Date: 14 Apr 2026.
 *  Purpose: Balancing between privacy and compatibility.
 *  License: MIT.
 * ==========================================
*/


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
user_pref("geo.provider.use_gpsd", true);

// ------------------------------------------
// Referer & DoH Control
// ------------------------------------------
user_pref("network.dns.disablePrefetch", true);
user_pref("network.http.referer.trimmingPolicy", 1);
user_pref("network.http.referer.XOriginTrimmingPolicy", 2);
user_pref("network.prefetch-next", false);
user_pref("network.trr.mode", 1);

// ------------------------------------------
// Resist Fingerprinting Control
// ------------------------------------------
user_pref("privacy.fingerprintingProtection", true);
user_pref("privacy.firstparty.isolate", true);
user_pref("privacy.globalprivacycontrol.enabled", true);
user_pref("privacy.globalprivacycontrol.was_ever_enabled", true);
user_pref("privacy.trackingprotection.emailtracking.enabled", true);
user_pref("privacy.trackingprotection.enabled", true);
user_pref("privacy.trackingprotection.socialtracking.enabled", true);
user_pref("privacy.resistFingerprinting.letterboxing.didForceSize", true);
user_pref("privacy.resistFingerprinting.letterboxing.gradient", true);
user_pref("privacy.resistFingerprinting.letterboxing.rememberSize", false);
user_pref("privacy.resistFingerprinting.letterboxing.vcenter", true);
user_pref("privacy.resistFingerprinting.pbmode", false);
user_pref("privacy.resistFingerprinting.randomDataOnCanvasExtract", true);