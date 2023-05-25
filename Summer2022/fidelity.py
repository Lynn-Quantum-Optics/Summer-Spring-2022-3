from helperFunc import *
from calculate_witness import *
from compile_measurements import * 
from scipy.linalg import sqrtm
from datetime import datetime

phiPlus = 1/math.sqrt(2) * np.array([[1],[0],[0],[1]])
phiMinus = 1/math.sqrt(2) * np.array([[1],[0],[0],[-1]])
psiPlus = 1/math.sqrt(2) * np.array([[0],[1],[1],[0]])
psiMinus = 1/math.sqrt(2) * np.array([[0],[1],[-1],[0]])

# return |Psi_W><Psi_W| for six quantum states associated with W
def W1(a,b):
  psi1 = np.add(a*phiPlus, b*phiMinus)
  return np.dot(psi1, psi1.conj().T)
def W2(a,b):
  psi2 = np.add(a*psiPlus, b*psiMinus)
  return np.dot(psi2, psi2.conj().T)
def W3(a,b):
  psi3 = np.add(a*phiPlus, b*psiPlus)
  return np.dot(psi3, psi3.conj().T)
def W4(a,b):
  psi4 = np.add(a*phiMinus, b*psiMinus)
  return np.dot(psi4, psi4.conj().T)
def W5(a,b):
  psi5 = np.add(a*phiPlus, b*1j*psiMinus)
  return np.dot(psi5, psi5.conj().T)
def W6(a,b):
  psi6 = np.add(a*phiMinus, b*1j*psiPlus)
  return np.dot(psi6, psi6.conj().T)

mat_list = [W1,W2,W3,W4,W5,W6]

# Calculate the fidelity of two states
def cal_fid(rho1, rho2):
  sqrt_rho1 = sqrtm(rho1)
  x = np.dot(sqrt_rho1, np.dot(rho2,sqrt_rho1))
  fid = np.trace(sqrtm(x))
  return fid**2

# Calculates the fidelity assuming one density matrix represents a pure state
def fid_1pure(rho1, rho2):
  fidelity = np.trace(np.dot(rho1, rho2))
  return fidelity

# calculates the fidelity of measured state with Bell States
def bellFid(exportCSV = False, date = datetime.now().strftime("%m/%d/%Y__%H:%M:%S")):
  c = compile(False)
  rho1 = densityMatrix(c)

  psi_plus = ["Psi Plus", np.array([[0, 0, 0, 0], [0, 0.5, 0.5, 0], [0, 0.5, 0.5, 0], [0, 0, 0, 0]])]
  psi_minus = ["Psi Minus", np.array([[0, 0, 0, 0], [0, 0.5, -0.5, 0], [0, -0.5, 0.5, 0], [0, 0, 0, 0]])]
  phi_plus = ["Phi Plus", np.array([[0.5, 0, 0, 0.5], [0, 0, 0, 0], [0, 0, 0, 0], [0.5, 0, 0, 0.5]])]
  phi_minus = ["Phi Minus", np.array([[0.5, 0, 0, -0.5], [0, 0, 0, 0], [0, 0, 0, 0], [-0.5, 0, 0, 0.5]])]

  bell_states = [psi_plus, psi_minus, phi_plus, phi_minus]

  bell_fid = []
  for state in bell_states:
    bell_fid += [[state[0], fid_1pure(rho1, state[1])]]
  
  df = pd.DataFrame(bell_fid, columns = ['Bell State', 'fidelity'])
  if exportCSV:
    name = date + '_Bell_Fidelity.csv'
    df.to_csv(name, index=False)
    print("Created Bell fidelity file with name: ", name)
  
  return bell_fid
