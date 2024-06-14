from conn import GenericConn
from multiprocessing import Pool
import time

def crear_txt(nombre_producto):
    ruta = f'outputs/{nombre_producto}.txt'
    with open(ruta,"w") as file:
        file.write(nombre_producto)
        time.sleep(5)
        
def main():
    conn = GenericConn()
    q_productos = 'SELECT * FROM Productos'
    df_productos = conn.get_query(q_productos)
    
    arr_productos = []
    for i,r in df_productos.iterrows():
        nombre_producto = r['Nombre']
        # crear_txt(nombre_producto)
        arr_productos.append(nombre_producto)
        
    print(arr_productos)
    pool = Pool(8)
    pool.map(crear_txt, arr_productos)
    pool.close()
    pool.join()



if __name__=='__main__':
    main()