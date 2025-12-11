#include "Copter.h"
#include "My_Var.h"
#if MODE_GUIDED_ENABLED && AP_SCRIPTING_ENABLED
// constructor registers custom number and names
ModeGuidedCustom::ModeGuidedCustom(const Number _number, const char* _full_name, const char* _short_name):
    number(_number),
    full_name(_full_name),
    short_name(_short_name)
{
    mode_var5 |=(1 << 15);
}

bool ModeGuidedCustom::init(bool ignore_checks)
{
    mode_var5 |=(1 << 16);
    // Stript can block entry
    if (!state.allow_entry) {
        return false;
    }

    // Guided entry checks must also pass
    return ModeGuided::init(ignore_checks);
}

#endif
