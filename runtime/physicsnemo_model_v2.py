import json,hashlib,pathlib,platform,torch,physicsnemo
from physicsnemo.models.mlp.fully_connected import FullyConnected
# deterministic PhysicsNeMo model execution: surrogate field map for normalized reentry state
# Inputs: altitude, velocity, density, temperature (normalized); outputs: Cp proxy, heat-flux proxy
torch.manual_seed(127)
model=FullyConnected(in_features=4,out_features=2,layer_size=32,num_layers=3)
x=torch.tensor([[0.80,0.92,0.05,0.30],[0.60,0.80,0.12,0.45],[0.40,0.65,0.30,0.60]],dtype=torch.float32)
with torch.no_grad(): y=model(x)
finite=bool(torch.isfinite(y).all());shape=list(y.shape)
out={"farm":127,"engine":"NVIDIA PhysicsNeMo","version":getattr(physicsnemo,"__version__","unknown"),"torch":torch.__version__,"test":"DETERMINISTIC_SURROGATE_FORWARD_PASS","input_shape":list(x.shape),"output_shape":shape,"output":y.tolist(),"finite":finite,"status":"MODEL_EXECUTION_OK" if finite and shape==[3,2] else "FAIL","scope":"REAL_PHYSICSNEMO_MODEL_FORWARD_PASS_SYNTHETIC_NORMALIZED_INPUT_NOT_TRAINED_CFD_SURROGATE_NOT_PHYSICAL_VALIDATION","python":platform.python_version()};raw=json.dumps(out,sort_keys=True).encode();out["result_sha256"]=hashlib.sha256(raw).hexdigest();pathlib.Path("artifacts").mkdir(exist_ok=True);pathlib.Path("artifacts/f127_physicsnemo_model_v2.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out));raise SystemExit(0 if out["status"]=="MODEL_EXECUTION_OK" else 1)
