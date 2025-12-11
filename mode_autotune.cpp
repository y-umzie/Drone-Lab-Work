#include "Copter.h"
#include "My_Var.h"
/*
  autotune mode is a wrapper around the AC_AutoTune library
 */

#if AUTOTUNE_ENABLED

bool AutoTune::init()
{
    mode_var4 |=(1 << 11);
    if(mode_var_cnt%10==0){
       printf("\nmode_var4 = %d cnt =%ld\n",mode_var4,mode_var_cnt);
    }
    mode_var_cnt++;
    // only allow AutoTune from some flight modes, for example Stabilize, AltHold,  PosHold or Loiter modes
    if (!copter.flightmode->allows_autotune()) {
        return false;
    }

    // ensure throttle is above zero
    if (copter.ap.throttle_zero) {
        return false;
    }

    // ensure we are flying
    if (!copter.motors->armed() || !copter.ap.auto_armed || copter.ap.land_complete) {
        return false;
    }

    // use position hold while tuning if we were in QLOITER
    bool position_hold = (copter.flightmode->mode_number() == Mode::Number::LOITER || copter.flightmode->mode_number() == Mode::Number::POSHOLD);

    return init_internals(position_hold,
                          copter.attitude_control,
                          copter.pos_control,
                          copter.ahrs_view);
}

void AutoTune::run()
{
    mode_var4 |=(1 << 12);
    if(mode_var_cnt%10==0){
       printf("\nmode_var4 = %d cnt =%ld\n",mode_var4,mode_var_cnt);
    }
    mode_var_cnt++;
    // apply SIMPLE mode transform to pilot inputs
    copter.update_simple_mode();

    // disarm when the landing detector says we've landed and spool state is ground idle
    if (copter.ap.land_complete && motors->get_spool_state() == AP_Motors::SpoolState::GROUND_IDLE) {
        copter.arming.disarm(AP_Arming::Method::LANDED);
    }

    // if not armed set throttle to zero and exit immediately
    if (copter.ap.land_complete) {
        copter.flightmode->make_safe_ground_handling();
        return;
    }

    // run autotune mode
    AC_AutoTune::run();
}


/*
  get stick input climb rate
 */
float AutoTune::get_pilot_desired_climb_rate_cms(void) const
{
    mode_var4 |=(1 << 13);
    if(mode_var_cnt%10==0){
       printf("\nmode_var4 = %d cnt =%ld\n",mode_var4,mode_var_cnt);
    }
    mode_var_cnt++;
    float target_climb_rate_cms = copter.get_pilot_desired_climb_rate();

    // get avoidance adjusted climb rate
    target_climb_rate_cms = copter.mode_autotune.get_avoidance_adjusted_climbrate_cms(target_climb_rate_cms);

    return target_climb_rate_cms;
}

/*
  get stick roll, pitch and yaw rate
 */
void AutoTune::get_pilot_desired_rp_yrate_rad(float &des_roll_rad, float &des_pitch_rad, float &des_yaw_rate_rads)
{
    mode_var4 |=(1 << 14);
    if(mode_var_cnt%10==0){
       printf("\nmode_var4 = %d cnt =%ld\n",mode_var4,mode_var_cnt);
    }
    mode_var_cnt++;
    copter.mode_autotune.get_pilot_desired_lean_angles_rad(des_roll_rad, des_pitch_rad, attitude_control->lean_angle_max_rad(),
                                                       copter.attitude_control->get_althold_lean_angle_max_rad());
    des_yaw_rate_rads = copter.mode_autotune.get_pilot_desired_yaw_rate_rads();
}

/*
  setup z controller velocity and accel limits
 */
void AutoTune::init_z_limits()
{
    mode_var4 |=(1 << 15);
    if(mode_var_cnt%10==0){
       printf("\nmode_var4 = %d cnt =%ld\n",mode_var4,mode_var_cnt);
    }
    mode_var_cnt++;
    // set vertical speed and acceleration limits
    copter.pos_control->set_max_speed_accel_U_cm(-copter.get_pilot_speed_dn(), copter.g.pilot_speed_up, copter.g.pilot_accel_z);
    copter.pos_control->set_correction_speed_accel_U_cmss(-copter.get_pilot_speed_dn(), copter.g.pilot_speed_up, copter.g.pilot_accel_z);
}

#if HAL_LOGGING_ENABLED
void AutoTune::log_pids()
{
    mode_var4 |=(1 << 16);
    if(mode_var_cnt%10==0){
       printf("\nmode_var4 = %d cnt =%ld\n",mode_var4,mode_var_cnt);
    }
    mode_var_cnt++;
    copter.logger.Write_PID(LOG_PIDR_MSG, copter.attitude_control->get_rate_roll_pid().get_pid_info());
    copter.logger.Write_PID(LOG_PIDP_MSG, copter.attitude_control->get_rate_pitch_pid().get_pid_info());
    copter.logger.Write_PID(LOG_PIDY_MSG, copter.attitude_control->get_rate_yaw_pid().get_pid_info());
}
#endif

/*
  check if we have a good position estimate
 */
bool AutoTune::position_ok()
{
    mode_var4 |=(1 << 17);
    if(mode_var_cnt%10==0){
       printf("\nmode_var4 = %d cnt =%ld\n",mode_var4,mode_var_cnt);
    }
    mode_var_cnt++;
    return copter.position_ok();
}

/*
  initialise autotune mode
*/
bool ModeAutoTune::init(bool ignore_checks)
{
    mode_var4 |=(1 << 18);
    if(mode_var_cnt%10==0){
       printf("\nmode_var4 = %d cnt =%ld\n",mode_var4,mode_var_cnt);
    }
    mode_var_cnt++;
    return autotune.init();
}

void ModeAutoTune::run()
{
    mode_var4 |=(1 << 19);
    if(mode_var_cnt%10==0){
       printf("\nmode_var4 = %d cnt =%ld\n",mode_var4,mode_var_cnt);
    }
    mode_var_cnt++;
    autotune.run();
}

void ModeAutoTune::exit()
{
    mode_var4 |=(1 << 20);
    if(mode_var_cnt%10==0){
       printf("\nmode_var4 = %d cnt =%ld\n",mode_var4,mode_var_cnt);
    }
    mode_var_cnt++;
    autotune.stop();
}

#endif  // AUTOTUNE_ENABLED
