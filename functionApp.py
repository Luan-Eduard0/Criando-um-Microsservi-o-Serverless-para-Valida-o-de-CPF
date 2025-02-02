import azure.functions as az
import logging
import re

def isValidCpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)  
    
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    def calculateDigit(cpf_slice, factor):
        total = sum(int(digit) * (factor - i) for i, digit in enumerate(cpf_slice))
        return (total * 10 % 11) % 10
    
    return (
        calculateDigit(cpf[:9], 10) == int(cpf[9]) and
        calculateDigit(cpf[:10], 11) == int(cpf[10])
    )

app = az.FunctionApp(http_auth_level=az.AuthLevel.FUNCTION)

@app.route(route="cpfvalidator")
def cpfvalidator(req: az.HttpRequest) -> az.HttpResponse:

    try:
        cpf = req.params.get('cpf') or (req.get_json().get('cpf') if req.get_json(silent=True) else None)
        
        if cpf and isValidCpf(cpf):
            return az.HttpResponse(f"CPF: {cpf} é valido")
        return az.HttpResponse("CPF INVALIDO.", status_code=400)
    except Exception as e:
  
        return az.HttpResponse("Internal Server Error", status_code=500)
