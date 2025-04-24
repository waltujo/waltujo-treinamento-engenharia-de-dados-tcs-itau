import sqlite3
import random
import datetime
from faker import Faker
import os
import logging as log
from typing import List, Tuple

def create_database(db_name: str) -> None:
    """Create database schema with four tables if they don't exist."""
    log.info("Creating database schema")
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        log.debug("Enabling foreign keys")
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Começar transação
        log.debug("Starting transaction for schema creation")
        
        log.info("Creating user table")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            birth_date TEXT,
            creation_date TEXT NOT NULL
        )
        ''')
        
        log.info("Creating product table")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            stock INTEGER DEFAULT 0,
            creation_date TEXT NOT NULL
        )
        ''')
        
        log.info("Creating order table")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS "order" (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            total_value REAL NOT NULL,
            creation_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
        ''')
        
        log.info("Creating order_item table")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_item (
            id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            creation_date TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES "order" (id),
            FOREIGN KEY (product_id) REFERENCES product (id)
        )
        ''')
        
        # Confirmar transação
        conn.commit()
        log.info("Database schema created successfully")
        
    except sqlite3.Error as e:
        # Reverter em caso de erro
        if conn:
            conn.rollback()
        log.error(f"Error creating database schema: {e}")
        raise
    finally:
        # Fechar conexão
        if conn:
            conn.close()

def generate_data(db_name: str) -> Tuple[int, int, int, int]:
    """Generate all data in a single transaction.
    
    Args:
        db_name: Database file name
        
    Returns:
        Tuple[int, int, int, int]: Number of users, products, orders, and order items created
    """
    log.info("Starting data generation in a single transaction")
    
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Habilitar chaves estrangeiras
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Obter timestamp atual para todas as inserções
        current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log.info(f"Using current timestamp for all records: {current_timestamp}")
        
        # Quantidades aleatórias para gerar
        user_quantity: int = random.randint(1, 10)
        product_quantity: int = random.randint(1, 8)
        order_quantity: int = random.randint(0, 1000)
        
        log.info(f"Will generate: {user_quantity} users, {product_quantity} products, {order_quantity} orders")
        
        # Iniciar Faker
        fake = Faker()
        
        # Gerar usuários
        log.info(f"Generating {user_quantity} users")
        users_created: int = 0
        for _ in range(user_quantity):
            name: str = fake.name()
            email: str = fake.email()
            phone: str = fake.phone_number()
            birth_date: str = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d')
            
            try:
                cursor.execute('''
                INSERT INTO user (name, email, phone, birth_date, creation_date)
                VALUES (?, ?, ?, ?, ?)
                ''', (name, email, phone, birth_date, current_timestamp))
                users_created += 1
                log.debug(f"Created user: {name} with email: {email}")
            except sqlite3.IntegrityError:
                log.warning(f"Duplicate email detected: {email}. Skipping...")
                continue
        
        # Gerar produtos
        log.info(f"Generating {product_quantity} products")
        products_created: int = 0
        categories: List[str] = ['Electronics', 'Clothing', 'Books', 'Home & Decor', 'Sports', 'Food']
        
        for _ in range(product_quantity):
            name: str = fake.word().capitalize() + ' ' + fake.word()
            description: str = fake.text(max_nb_chars=200)
            price: float = round(random.uniform(10.0, 1000.0), 2)
            category: str = random.choice(categories)
            stock: int = random.randint(0, 100)
            
            cursor.execute('''
            INSERT INTO product (name, description, price, category, stock, creation_date)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, description, price, category, stock, current_timestamp))
            products_created += 1
            log.debug(f"Created product: {name} in category {category}")
        
        # Verificar se temos usuários e produtos para gerar pedidos
        cursor.execute("SELECT id FROM user")
        user_ids: List[int] = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id, price FROM product")
        products_info: List[Tuple[int, float]] = cursor.fetchall()
        
        if not user_ids or not products_info:
            raise ValueError("No users or products available after insertion. Cannot create orders.")
        
        # Gerar pedidos e garantir que cada pedido tenha pelo menos um item
        log.info(f"Generating {order_quantity} orders, each with at least one item")
        orders_created: int = 0
        items_created: int = 0
        status_options: List[str] = ['pending', 'approved', 'shipped', 'delivered', 'canceled']
        
        for i in range(order_quantity):
            user_id: int = random.choice(user_ids)
            days_ago: int = random.randint(0, 365)
            order_date: str = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
            status: str = random.choice(status_options)
            
            # Criar pedido com valor total zero inicialmente
            cursor.execute('''
            INSERT INTO "order" (user_id, order_date, status, total_value, creation_date)
            VALUES (?, ?, ?, 0, ?)
            ''', (user_id, order_date, status, current_timestamp))
            
            order_id: int = cursor.lastrowid # type: ignore
            orders_created += 1
            
            # Adicionar pelo menos um item para este pedido
            product_id, base_price = random.choice(products_info)
            quantity: int = random.randint(1, 5)
            unit_price: float = round(base_price * random.uniform(0.9, 1.1), 2)
            
            cursor.execute('''
            INSERT INTO order_item (order_id, product_id, quantity, unit_price, creation_date)
            VALUES (?, ?, ?, ?, ?)
            ''', (order_id, product_id, quantity, unit_price, current_timestamp))
            items_created += 1
            
            # Calcular valor total inicial do pedido
            total_value: float = quantity * unit_price
            
            # Adicionar itens extras aleatoriamente (0 a 3 itens extras)
            extra_items: int = random.randint(0, 3)
            
            for _ in range(extra_items):
                # Certificar-se de que não escolhemos o mesmo produto novamente
                available_products = [p for p in products_info if p[0] != product_id]
                if not available_products:  # Se não houver outros produtos disponíveis
                    available_products = products_info  # Permitir duplicatas
                    
                product_id, base_price = random.choice(available_products)
                quantity = random.randint(1, 3)
                unit_price = round(base_price * random.uniform(0.9, 1.1), 2)
                
                cursor.execute('''
                INSERT INTO order_item (order_id, product_id, quantity, unit_price, creation_date)
                VALUES (?, ?, ?, ?, ?)
                ''', (order_id, product_id, quantity, unit_price, current_timestamp))
                items_created += 1
                
                # Atualizar valor total
                total_value += quantity * unit_price
            
            # Atualizar o valor total do pedido
            cursor.execute('''
            UPDATE "order" SET total_value = ? WHERE id = ?
            ''', (round(total_value, 2), order_id))
            
            if i % 100 == 0 and i > 0:
                log.info(f"Created {i} orders so far...")
        
        # Confirmar transação
        conn.commit()
        log.info(f"Transaction committed successfully. Created {users_created} users, {products_created} products, {orders_created} orders, {items_created} order items")
        
        return users_created, products_created, orders_created, items_created
        
    except Exception as e:
        # Reverter em caso de erro
        if conn:
            conn.rollback()
        log.error(f"Error during data generation: {e}")
        log.error("All changes have been rolled back")
        raise
    finally:
        # Fechar conexão
        if conn:
            conn.close()

def show_insertion_statistics(users_created: int, products_created: int, orders_created: int, order_items_created: int) -> None:
    """Display statistics about the data inserted in this run.
    
    Args:
        users_created: Number of users created
        products_created: Number of products created
        orders_created: Number of orders created
        order_items_created: Number of order items created
    """
    log.info("Displaying insertion statistics")
    log.info("=== DATA INSERTION STATISTICS ===")
    log.info(f"Users created: {users_created}")
    log.info(f"Products created: {products_created}")
    log.info(f"Orders created: {orders_created}")
    log.info(f"Order items created: {order_items_created}")
    log.info(f"Average items per order: {order_items_created / orders_created:.2f}")

def check_tables_exist(db_name: str) -> bool:
    """Check if all required tables exist in the database.
    
    Args:
        db_name: Database file name
        
    Returns:
        bool: True if all tables exist, False otherwise
    """
    required_tables = ["user", "product", "order", "order_item"]
    
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Get list of tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        # Check if all required tables exist
        for table in required_tables:
            if table not in existing_tables and table != "order":
                return False
            elif table == "order" and "order" not in existing_tables:
                return False
        
        return True
    except sqlite3.Error as e:
        log.error(f"Error checking tables: {e}")
        return False
    finally:
        if conn:
            conn.close()
            
def main() -> None:
    """Main function to run the database generator."""
    # Constants
    DB_NAME: str = './4 - ecommerce/data/ecommerce.db'
    
    # Configure logging
    log.basicConfig(
        level=log.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Criar diretório se não existir
    os.makedirs('./4 - ecommerce/data', exist_ok=True)
    
    log.info("Starting database generation process")
    
    try:
        database_exists: bool = os.path.exists(DB_NAME)
        
        # Check if database exists and has required tables
        if database_exists:
            tables_exist = check_tables_exist(DB_NAME)
            if tables_exist:
                log.info(f"Database '{DB_NAME}' already exists with all required tables")
            else:
                log.info(f"Database '{DB_NAME}' exists but is missing some tables. Creating tables...")
                create_database(DB_NAME)
        else:
            log.info(f"Database '{DB_NAME}' does not exist, will create it")
            create_database(DB_NAME)
        
        # Generate all data in a single transaction
        log.info("Generating new data...")
        users_created, products_created, orders_created, order_items_created = generate_data(DB_NAME)
        
        # Show statistics only for this run
        show_insertion_statistics(users_created, products_created, orders_created, order_items_created)
        
        if not database_exists:
            log.info(f"Database '{DB_NAME}' created successfully!")
        else:
            log.info(f"New data added to database '{DB_NAME}'!")
        
        log.info("Database generation process completed successfully")
        
    except Exception as e:
        log.error(f"An error occurred: {e}")
        log.error("No data was inserted due to the error.")
        return


if __name__ == "__main__":
    main()