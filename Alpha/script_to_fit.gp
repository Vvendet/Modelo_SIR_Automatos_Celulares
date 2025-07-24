# fit_script.gp
set terminal pngcairo
set output 'fit_result.png'

# Define the model
f(x)=(a-1)*b**(a-1)*x**(-a) + 10

# Initial guesses for parameters
a = 2.30101992240304
b = 1905.0

# Fit the model to the data
fit f(x) 'Ixalpha.dat' via a,b

# Plot the data and the fitted function
plot 'Ixalpha.dat' with points,f(x) title sprintf('Fit: y = %.2fx + %.2f', a, b) with lines
