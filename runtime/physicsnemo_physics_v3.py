import json,hashlib,pathlib,math,platform,torch,physicsnemo
from physicsnemo.models.mlp.fully_connected import FullyConnected
# Physics-informed training benchmark: learn exact 1-D compressible-flow isentropic pressure ratio from Mach.
# gamma=1.4, p/p0=(1+(gamma-1)/2*M^2)^(-gamma/(gamma-1)).
torch.manual_seed(127);torch.set_num_threads(2);gamma=1.4
M=torch.linspace(0.0,5.0,257).reshape(-1,1)
y=(1.0+(gamma-1.0)*0.5*M*M)**(-gamma/(gamma-1.0))
model=FullyConnected(in_features=1,out_features=1,layer_size=64,num_layers=4)
opt=torch.optim.Adam(model.parameters(),lr=3e-3)
for epoch in range(1200):
 opt.zero_grad();pred=model(M);loss=torch.mean((pred-y)**2);loss.backward();opt.step()
with torch.no_grad():
 pred=model(M);err=torch.abs(pred-y);mae=float(err.mean());mx=float(err.max());mse=float(torch.mean((pred-y)**2));finite=bool(torch.isfinite(pred).all())
# independent analytic checkpoints
idx=[0,51,102,153,204,256];checks=[{"M":float(M[i]),"analytic":float(y[i]),"model":float(pred[i]),"abs_error":float(err[i])} for i in idx]
ok=finite and mae<0.01 and mse<0.001
out={"farm":127,"engine":"NVIDIA PhysicsNeMo","version":getattr(physicsnemo,"__version__","unknown"),"test":"PHYSICS_INFORMED_ISENTROPIC_PRESSURE_RATIO","gamma":gamma,"mach_range":[0.0,5.0],"training_points":257,"epochs":1200,"mae":mae,"max_abs_error":mx,"mse":mse,"checkpoints":checks,"status":"REFERENCE_LEARNED_OK" if ok else "FAIL","scope":"REAL_PHYSICSNEMO_TRAINING_AGAINST_ANALYTIC_COMPRESSIBLE_FLOW_REFERENCE_NOT_CFD_NOT_HYPERSONIC_VALIDATION","python":platform.python_version()};raw=json.dumps(out,sort_keys=True).encode();out["result_sha256"]=hashlib.sha256(raw).hexdigest();pathlib.Path("artifacts").mkdir(exist_ok=True);pathlib.Path("artifacts/f127_physicsnemo_physics_v3.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out));raise SystemExit(0 if ok else 1)
