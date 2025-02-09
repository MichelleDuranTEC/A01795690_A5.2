# pylint: disable=invalid-name


"""Ejercicio de Compute_Sales"""
import json
import sys
import time


def load_json(file_path):
    """Carga un archivo JSON y maneja posibles errores."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {file_path}")
    except json.JSONDecodeError:
        print(f"Error: El archivo {file_path} no tiene un formato JSON válido")
    return None


def compute_total_sales(price_catalogue, sales_record):
    """Calcula el costo total de todas las ventas"""
    total = 0.0
    invalid_entries = []
    product_total = {}

    # Convertir catálogo de precios en un diccionario {nombre_producto: precio}
    price_dict = {item["title"].strip().lower():
                  item["price"] for item in price_catalogue}

    for sale in sales_record:
        product = sale.get("Product", "").strip().lower()  # Normalizar nombres
        quantity = sale.get("Quantity")
        if product in price_dict and isinstance(quantity, (int, float)):
            total += price_dict[product] * quantity

            # Contar cuántos productos de cada tipo se vendieron
            product_total[product] = product_total.get(
                product, 0) + quantity
        else:
            invalid_entries.append(sale)
    return total, invalid_entries, product_total, price_dict


def main():
    """Función principal que ejecuta el programa."""
    if len(sys.argv) != 3:
        print("Uso: python computeSales.py"
              "priceCatalogue.json salesRecord.json")
        return
    price_file, sales_file = sys.argv[1], sys.argv[2]
    start_time = time.time()
    price_catalogue = load_json(price_file)
    sales_record = load_json(sales_file)
    if price_catalogue is None or sales_record is None:
        return
    total, invalid_entries, product_total, price_dict = compute_total_sales(
        price_catalogue, sales_record)
    elapsed_time = time.time() - start_time

    # Ordenar productos alfabéticamente
    products_sold = "\n".join([f"- {product.title()} ({
        quantity} piezas de ${price_dict[product]:.2f} c/u)"
                    for product, quantity in sorted(product_total.items())])

    output = [
        "RESULTADOS DE LAS VENTAS",
        f"Costo total de ventas: ${total:.2f}",
        f"Tiempo de ejecución: {elapsed_time:.4f} segundos",
        "Productos vendidos:",
        products_sold if products_sold else "No se vendieron productos.",
        "Errores encontrados en los datos:",
        json.dumps(invalid_entries, indent=4)
    ]
    output_text = "\n".join(output)
    print(output_text)
    with open("SalesResults.txt", "w", encoding="utf-8") as result_file:
        result_file.write(output_text)


if __name__ == "__main__":
    main()
