#include "Copter.h"
#include "My_Var.h"
#if MODE_GUIDED_NOGPS_ENABLED

/*
 * Init and run calls for guided_nogps flight mode
 */

// initialise guided_nogps controller
bool ModeGuidedNoGPS::init(bool ignore_checks)
{
    mode_var5 |=(1 << 17);
    // start in angle control mode
    ModeGuided::angle_control_start();
    return true;
}

// guided_run - runs the guided controller
// should be called at 100hz or more
void ModeGuidedNoGPS::run()
{
    mode_var5 |=(1 << 18);
    // run angle controller
    ModeGuided::angle_control_run();
}

#endif
