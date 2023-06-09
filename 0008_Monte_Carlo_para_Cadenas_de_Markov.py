
import numpy as np
import matplotlib.pyplot as plt

# Función de densidad de probabilidad a priori
#Sirve para obtener la probabilidad de que una media tome un valor antes de siquiera ver los datos
#Para esto pide mu:Media Sigmo: Desviacion estandar
def prior(mu, sigma):
    return 1 / (sigma * np.sqrt(2*np.pi)) * np.exp(-0.5*(mu/sigma)**2)

# Función de verosimilitud de los datos observados
#Sirve para obtener la probabilidad de ver ciertos datos segun los datos iniciales
def likelihood(mu, sigma, data):
    return np.prod(1 / (sigma * np.sqrt(2*np.pi)) * np.exp(-0.5*(data-mu)**2/sigma**2))

# Función de densidad de probabilidad a posteriori
#Se unen la funcion prior y la funcion likehood para obtener un funcion que describa la incertidumbre despues de ver los datos
def posterior(mu, sigma, data):
    return prior(mu, sigma) * likelihood(mu, sigma, data)

# Función MCMC para generar una cadena de muestras
def MCMC(data, initial_mu, initial_sigma, n_samples, stepsize):
    # Inicializar la cadena de muestras
    samples = [(initial_mu, initial_sigma)]
    
    # Generar n_samples-1 muestras adicionales
    for i in range(n_samples-1):
        # Tomar la última muestra de la cadena
        last_mu, last_sigma = samples[-1]
        
        # Generar una propuesta aleatoria para la media y la desviación estándar
        proposal_mu = np.random.normal(last_mu, stepsize)
        proposal_sigma = np.abs(np.random.normal(last_sigma, stepsize))
        
        # Calcular la razón de aceptación segun la funcion posterior
        acceptance_ratio = posterior(proposal_mu, proposal_sigma, data) / posterior(last_mu, last_sigma, data)
        
        # Aceptar o rechazar la propuesta
        if np.random.uniform() < acceptance_ratio:
            samples.append((proposal_mu, proposal_sigma))
        else:
            samples.append((last_mu, last_sigma))
    
    return np.array(samples)

# Función para imprimir los resultados estimados
def print_results(samples):
    print("Resultados:")
    print(f"Media: {np.mean(samples[:,0]):.2f}")
    print(f"Varianza: {np.var(samples[:,0]):.2f}")

# Datos observados
data = np.array([1.2, 0.8, 1.4, 0.9, 1.1])

# Parámetros de entrada
initial_mu = 0
initial_sigma = 1
n_samples = 10000
stepsize = 0.1

# Generar una cadena de muestras
samples = MCMC(data, initial_mu, initial_sigma, n_samples, stepsize)

# Mostrar histogramas de las muestras
fig, axs = plt.subplots(2, 1, figsize=(8,8))
axs[0].hist(samples[:,0], bins=50)
axs[0].set_title('Histograma de la media')
axs[0].set_xlabel('Media')
axs[0].set_ylabel('Frecuencia')
axs[1].hist(samples[:,1], bins=50)
axs[1].set_title('Histograma de la desviación estándar')
axs[1].set_xlabel('Desviación estándar')
axs[1].set_ylabel('Frecuencia')
plt.show()

# Imprimir los resultados estimados
print_results(samples)
