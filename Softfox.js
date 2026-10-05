
/****************************************************************************************
 * Softfox                                                                            *
 * "SHIMORA"                                                                          *
 * priority: smooth scrolling                                                         *
 * version: 157                                                                       *
 * url: https://github.com/SHIMORA-6600X/ZenFox                                       *
 * license: MIT                                                                       *
 ***************************************************************************************/

// [PICK ONE] Uncomment only ONE option block below. Leave the other four commented.
// Reset procedure when switching: close Firefox, open profile folder
// (about:profiles > Root Directory), delete the related lines from prefs.js
// or use about:support > Refresh Firefox, then apply the new option.

/****************************************************************************************
 * OPTION: SHARPEN SCROLLING [DISABLED - example]                                     *
 ****************************************************************************************/
// only sharpen scrolling
//user_pref("apz.overscroll.enabled", true); // DEFAULT NON-LINUX
//user_pref("general.smoothScroll", true); // DEFAULT
//user_pref("mousewheel.min_line_scroll_amount", 10); // adjust this number to your liking; default=5
//user_pref("general.smoothScroll.mouseWheel.durationMinMS", 80); // default=50
//user_pref("general.smoothScroll.currentVelocityWeighting", "0.15"); // default=.25
//user_pref("general.smoothScroll.stopDecelerationWeighting", "0.6"); // default=.4
// for Firefox Nightly only:
// [1] https://bugzilla.mozilla.org/show_bug.cgi?id=1846935
//user_pref("general.smoothScroll.msdPhysics.enabled", false); // [FF122+ Nightly]

/****************************************************************************************
 * OPTION: INSTANT SCROLLING (SIMPLE ADJUSTMENT) [DISABLED]                           *
 ****************************************************************************************/
// recommended for 60hz+ displays
//user_pref("apz.overscroll.enabled", true); // DEFAULT NON-LINUX
//user_pref("general.smoothScroll", true); // DEFAULT
//user_pref("mousewheel.default.delta_multiplier_y", 280); // 250-400; adjust this number to your liking
// for Firefox Nightly only:
// [1] https://bugzilla.mozilla.org/show_bug.cgi?id=1846935
//user_pref("general.smoothScroll.msdPhysics.enabled", false); // [FF122+ Nightly]

/****************************************************************************************
 * OPTION: SMOOTH SCROLLING [DISABLED]                                                *
 ****************************************************************************************/
// recommended for 90hz+ displays
//user_pref("apz.overscroll.enabled", true); // DEFAULT NON-LINUX
//user_pref("general.smoothScroll", true); // DEFAULT
//user_pref("general.smoothScroll.msdPhysics.enabled", true);
//user_pref("mousewheel.default.delta_multiplier_y", 320); // 250-400; adjust this number to your liking

/****************************************************************************************
 * OPTION: ZEN SMOOTH SCROLLING [ACTIVE - DEFAULT]                                    *
 ****************************************************************************************/
// recommended for 120hz+ displays
user_pref("general.smoothScroll.msdPhysics.enabled", true);
user_pref("general.smoothScroll.currentVelocityWeighting", "0.15");
user_pref("general.smoothScroll.stopDecelerationWeighting", "0.6");
user_pref("mousewheel.min_line_scroll_amount", 10);
user_pref("general.smoothScroll.mouseWheel.durationMinMS", 80);
user_pref("general.smoothScroll.msdPhysics.continuousMotionMaxDeltaMS", 12);
user_pref("general.smoothScroll.msdPhysics.motionBeginSpringConstant", 600);
user_pref("general.smoothScroll.msdPhysics.regularSpringConstant", 650);
user_pref("general.smoothScroll.msdPhysics.slowdownMinDeltaMS", 25);
user_pref("general.smoothScroll.msdPhysics.slowdownSpringConstant", 250);
user_pref("mousewheel.default.delta_multiplier_y", 210);

/****************************************************************************************
 * OPTION: NATURAL SMOOTH SCROLLING V3 [MODIFIED] [DISABLED]                          *
 ****************************************************************************************/
// recommended for 120hz+ displays
// largely matches Chrome flags: Windows Scrolling Personality and Smooth Scrolling
//user_pref("apz.overscroll.enabled", true); // DEFAULT NON-LINUX
//user_pref("general.smoothScroll", true); // DEFAULT
//user_pref("general.smoothScroll.msdPhysics.continuousMotionMaxDeltaMS", 12);
//user_pref("general.smoothScroll.msdPhysics.enabled", true);
//user_pref("general.smoothScroll.msdPhysics.motionBeginSpringConstant", 600);
//user_pref("general.smoothScroll.msdPhysics.regularSpringConstant", 650);
//user_pref("general.smoothScroll.msdPhysics.slowdownMinDeltaMS", 25);
//user_pref("general.smoothScroll.msdPhysics.slowdownMinDeltaRatio", "2");
//user_pref("general.smoothScroll.msdPhysics.slowdownSpringConstant", 250);
//user_pref("general.smoothScroll.currentVelocityWeighting", "1");
//user_pref("general.smoothScroll.stopDecelerationWeighting", "1");
//user_pref("mousewheel.default.delta_multiplier_y", 330); // 250-400; adjust this number to your liking
