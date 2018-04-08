D0 = 0.23;
R = 1.987;
Q = 32900;

prompt = 'what is the value for T?';

T = input(prompt) // temperature 900 - 1100
  
D = D0 * exp(-Q/(R*T))
  
Cs = 1.3;

prompt1 = 'what is the value for C0?'
  
C0 = input (prompt1) // 1018 .0018 1045 .0045
  
Cx = C0 + (1 * 10^-16);

z = (Cs-Cx) / (Cs-C0)
  
prompt3 = 'what is the value for t?'
  
t = input (prompt3) // time in minutes
  
x = 2 * erfinv(z) * (D*t)^(1/2)

