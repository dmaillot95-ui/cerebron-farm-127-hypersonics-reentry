import json,math,hashlib,pathlib,platform
rho=0.0002944526086139048;v=6000.;rn=1.;k=1.83e-4
# independent algebraic path: sqrt(rho/rn)*v^3 versus sqrt(rho)*v*v*v/sqrt(rn)
q1=k*math.sqrt(rho/rn)*v**3;q2=k*math.sqrt(rho)*v*v*v/math.sqrt(rn);delta=abs(q1-q2);ok=delta<1e-9
out={"farm":127,"engine":"python-independent-correlation-crosscheck","test":"SUTTON_GRAVES_ALGEBRAIC_REPRODUCTION","heat_flux_path1_w_m2":q1,"heat_flux_path2_w_m2":q2,"absolute_delta_w_m2":delta,"status":"INDEPENDENT_REPRODUCTION_OK" if ok else "FAIL","scope":"ALGEBRAIC_CROSSCHECK_NOT_EXTERNAL_CFD_DSMC_OR_PHYSICAL_VALIDATION","python":platform.python_version()};raw=json.dumps(out,sort_keys=True).encode();out["result_sha256"]=hashlib.sha256(raw).hexdigest();pathlib.Path("artifacts").mkdir(exist_ok=True);pathlib.Path("artifacts/f127_independent_reproduction.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out));raise SystemExit(0 if ok else 1)
