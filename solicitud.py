def solicitud ():
    import requests
    from bs4 import BeautifulSoup

    cookies = {'PHPSESSID': 'csbqv43ahca396h7oe5ppd2e5s', 'BANCLFAVV1': 'SU5ELklQU0FDLkJDU3xJUFNBfDE%3D%7CQ09NLkNPUFBFUi5GTXxDT0JSRSBGVVRVUk98Mg%3D%3D%7CQ1VSLlVTRC9DTFBTUE9ULkZNfFVTRC9DTFB8MQ%3D%3D%7CQ1VSLlVGUkVGLklTRi5GTXxVRnwx'}

    response = requests.post('https://indicadores.banchileinversiones.cl/www/v2/cookiescontroller.html', cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    valores = soup.find_all("td")
    lista, lista1, lista_aux, lista_str = [], [], [], []

    for i in valores:
        texto = i.find("span").text.lstrip().rstrip()
        lista1.append(texto)

    for i in range(len(lista1)):
        lista_aux.append(lista1[i])
        if i % 3 == 2:
            lista.append(lista_aux)
            lista_aux = []

    for i in lista:
        lista_str.append(" ".join(i))

    return lista_str
    #print(ahora)
    #for i in lista_str:
    #    print(i)