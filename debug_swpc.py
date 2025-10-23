<<<<<<< Updated upstream
<<<<<<< Updated upstream
﻿import traceback
try:
    from orchestrator.adapters import swpc
    print("Imported swpc OK")
    kp = swpc.fetch_kp_1m(6)
    print("Kp rows:", len(kp), "cols:", kp.columns.tolist())
    bundle = swpc.bundle(6)
    print("Bundle columns:", bundle.columns.tolist(), "rows:", len(bundle))
except Exception as e:
    print("ERROR:", e)
    traceback.print_exc()
=======
=======
>>>>>>> Stashed changes
﻿import traceback
try:
    from orchestrator.adapters import swpc
    print("Imported swpc OK")
    kp = swpc.fetch_kp_1m(6)
    print("Kp rows:", len(kp), "cols:", kp.columns.tolist())
    bundle = swpc.bundle(6)
    print("Bundle columns:", bundle.columns.tolist(), "rows:", len(bundle))
except Exception as e:
    print("ERROR:", e)
    traceback.print_exc()
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
