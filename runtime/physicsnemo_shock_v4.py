import json,hashlib,pathlib,math,platform,torch,physicsnemo
from physicsnemo.models.mlp.fully_connected import FullyConnected
# Normal-shock benchmark, gamma=1.4. Train PhysicsNeMo model against exact Rankine-Hugoniot relations.
torch.manual_seed(127);torch.set_num_threads(2);g=1.4
M=torch.linspace(1.05,8.0,384).reshape(-1,1)
rho=((g+1)*M*M)/((g-1)*M*M+2)
p=1+(2*g/(g+1))*(M*M-1)
t=p/rho
y=torch.cat([rho,p,t],dim=1)
# scale outputs to comparable magnitudes for stable learning
scale=torch.tensor([[6.0,75.0,15.0]]);ys=y/scale
model=FullyConnected(in_features=1,out_features=3,layer_size=96,num_layers=5)
opt=torch.optim.Adam(model.parameters(),lr=2e-3)
for epoch in range(1800):
 opt.zero_grad();pred=model(M);loss=torch.mean((pred-ys)**2);loss.backward();opt.step()
with torch.no_grad():
 pred=model(M)*scale;rel=torch.abs(pred-y)/torch.clamp(torch.abs(y),min=1e-6);mre=float(rel.mean());mx=float(rel.max());finite=bool(torch.isfinite(pred).all())
idx=[0,54,108,162,216,270,383];checks=[{"M1":float(M[i]),"exact":[float(q) for q in y[i]],"model":[float(q) for q in pred[i]],"max_rel_error":float(rel[i].max())} for i in idx]
ok=finite and mre<0.02 and mx<0.15
out={"farm":127,"engine":"NVIDIA PhysicsNeMo","version":getattr(physicsnemo,"__version__","unknown"),"test":"NORMAL_SHOCK_RANKINE_HUGONIOT","gamma":g,"mach_range":[1.05,8.0],"training_points":384,"epochs":1800,"outputs":["rho2_rho1","p2_p1","T2_T1"],"mean_relative_error":mre,"max_relative_error":mx,"checkpoints":checks,"status":"SHOCK_REFERENCE_LEARNED_OK" if ok else "FAIL","scope":"REAL_PHYSICSNEMO_TRAINING_AGAINST_EXACT_NORMAL_SHOCK_RELATIONS_NOT_CFD_NOT_CHEMICAL_NONEQUILIBRIUM_NOT_PHYSICAL_VALIDATION","python":platform.python_version()};raw=json.dumps(out,sort_keys=True).encode();out["result_sha256"]=hashlib.sha256(raw).hexdigest();pathlib.Path("artifacts").mkdir(exist_ok=True);pathlib.Path("artifacts/f127_physicsnemo_shock_v4.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out));raise SystemExit(0 if ok else 1)
