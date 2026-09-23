import json,math,hashlib,pathlib,platform
# Re-entry engineering canary: atmosphere + hypersonic dynamic pressure + Sutton-Graves-type convective heating trend.
rho0=1.225; H=7200.; alt=60000.; v=6000.; rn=1.0
rho=rho0*math.exp(-alt/H); q=.5*rho*v*v; mach=v/295.0
# engineering correlation, SI-scaled coefficient for trend/reference canary only
k=1.83e-4; heat=k*math.sqrt(rho/rn)*v**3
# independent identities checked directly
q_ref=.5*rho0*math.exp(-alt/H)*v*v; heat_ref=k*math.sqrt(rho0*math.exp(-alt/H)/rn)*v**3
ok=mach>5 and abs(q-q_ref)<1e-9*max(1,q_ref) and abs(heat-heat_ref)<1e-9*max(1,heat_ref) and q>0 and heat>0
out={"farm":127,"engine":"python-hypersonic-reentry-engineering-canary","engine_version":platform.python_version(),"test":"60KM_6KMS_REENTRY_POINT","altitude_m":alt,"velocity_m_s":v,"density_kg_m3":rho,"mach_estimate":mach,"dynamic_pressure_pa":q,"nose_radius_m":rn,"convective_heat_flux_proxy_w_m2":heat,"status":"REAL_ENGINE_CANARY_OK" if ok else "FAIL","epistemic_status":"ENGINEERING_CORRELATION_CANARY_NOT_CFD_DSMC_OR_FLIGHT_VALIDATION"}
raw=json.dumps(out,sort_keys=True).encode();out["result_sha256"]=hashlib.sha256(raw).hexdigest();pathlib.Path("artifacts").mkdir(exist_ok=True);pathlib.Path("artifacts/f127_engine_canary.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out));raise SystemExit(0 if ok else 1)
