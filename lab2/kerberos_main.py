import random
import time
from des_main import Des
from ast import literal_eval as make_tuple

# Получение текущего времени в миллисекундах
current_milli_time = lambda: int(round(time.time() * 1000))
# Преобразование часов в миллисекунды
hours_to_milli = lambda hour: hour * 3600 * 10000

class DesEncryptor:
    def encrypt_data(self, data, key):
        encrypted = Des().encrypt(key=str(key), text=str(data), padding=True)
        return encrypted

    def decrypt_data(self, data, key):
        decrypted = Des().decrypt(key=str(key), text=str(data), padding=True)
        decrypted = make_tuple(decrypted)
        return decrypted

class KeyGenerator:
    @staticmethod
    def generate_key():
        return random.randint(100000000, 999999999)

class KeyDistributionCenter:
    # Список доступных клиентов и серверов с их ключами
    available_clients = ['client1', 'client2']
    clients_keys = [KeyGenerator.generate_key(), KeyGenerator.generate_key()]
    available_servers = ['server1', 'server2']
    servers_keys = [KeyGenerator.generate_key(), KeyGenerator.generate_key()]

    def __init__(self):
        self.des = DesEncryptor()
        self.tgs_id = 1
        # Генерация ключа Ticket Granting Server (TGS)
        self.key_tgs = KeyGenerator.generate_key()

    def get_permission_ticket(self, client_id):
        if client_id not in self.available_clients:
            print('Unknown client id')
            return

        t = current_milli_time()
        p = hours_to_milli(48)
        key_tgs_c = KeyGenerator.generate_key()
        ticket = self.create_permission_ticket(client_id, self.tgs_id, t, p, key_tgs_c)

        encrypted_ticket = self.des.encrypt_data(ticket, self.key_tgs)
        bundle = (encrypted_ticket, key_tgs_c)

        index = self.available_clients.index(client_id)
        client_key = self.clients_keys[index]
        encrypted_bundle = self.des.encrypt_data(bundle, client_key)

        return encrypted_bundle

    def get_server_ticket(self, permission_ticket, authority, server_id):
        permission_ticket = self.des.decrypt_data(permission_ticket, self.key_tgs)
        client_id, _, t, p, key_tgs_c = permission_ticket

        authority = self.des.decrypt_data(authority, key_tgs_c)
        auth_client_id, auth_t = authority

        if client_id != auth_client_id:
            print('Invalid client')
            return None
        if not (t <= auth_t <= t + p):
            print('Expired')
            return None

        t = current_milli_time()
        p = hours_to_milli(48)
        key_ss_c = KeyGenerator.generate_key()
        server_ticket = self.create_server_ticket(client_id, server_id, t, p, key_ss_c)

        index = self.available_servers.index(server_id)
        server_key = self.servers_keys[index]

        encrypted_server_ticket = self.des.encrypt_data(server_ticket, server_key)
        bundle = (encrypted_server_ticket, key_ss_c)
        encrypted_bundle = self.des.encrypt_data(bundle, key_tgs_c)

        return encrypted_bundle

    @staticmethod
    def create_permission_ticket(client_id, tgs, t, p, key_tgs_c):
        return client_id, tgs, t, p, key_tgs_c

    @staticmethod
    def create_server_ticket(client_id, server_id, t, p, key_ss_c):
        return client_id, server_id, t, p, key_ss_c

class Client:
    def __init__(self, client_id, client_key, kdc, servers):
        self.client_id = client_id
        self.client_key = client_key
        self.kdc = kdc
        self.servers = servers
        self.des = DesEncryptor()
        self.permission_ticket = None
        self.key_tgs_c = None

    def make_server_call(self, server_number):
        server = self.servers[server_number]

        if self.permission_ticket is None or self.key_tgs_c is None:
            permission_ticket_bundle = self.kdc.get_permission_ticket(self.client_id)
            if permission_ticket_bundle is None:
                return

            permission_ticket_bundle = self.des.decrypt_data(permission_ticket_bundle, self.client_key)

            self.permission_ticket, self.key_tgs_c = permission_ticket_bundle[:2]

        permission_ticket = self.permission_ticket
        key_tgs_c = self.key_tgs_c

        bundle = self.request_tgs(permission_ticket, key_tgs_c, server.server_id)
        if bundle is None:
            return

        server_ticket, key_ss_c = self.des.decrypt_data(bundle, key_tgs_c)

        t = current_milli_time()
        authority = (self.client_id, t)
        authority_enctypted = self.des.encrypt_data(authority, key_ss_c)
        confirm_t = server.connect(server_ticket, authority_enctypted)
        if confirm_t is None:
            return

        confirm_t = self.des.decrypt_data(confirm_t, key_ss_c)
        if confirm_t != t + 1:
            print('Server returns an incorrect time label')
            return

        print('Server call succesful')

    def request_tgs(self, permission_ticket, key_tgs_c, server_id):
        encrypted_authority = self.des.encrypt_data((self.client_id, current_milli_time()), key_tgs_c)
        bundle = self.kdc.get_server_ticket(permission_ticket, encrypted_authority, server_id)
        return bundle


class Server:
    def __init__(self, server_id, server_key):
        self.server_id = server_id
        self.server_key = server_key
        self.des = DesEncryptor()

    def connect(self, server_ticket, authority):
        client_id, received_server_id, t, p, key_ss_c = self.des.decrypt_data(server_ticket, self.server_key)

        if received_server_id != self.server_id:
            print('Wrong server')
            return None

        auth_client_id, auth_t = self.des.decrypt_data(authority, key_ss_c)

        if client_id != auth_client_id:
            print('Invalid client')
            return None
        if not (t <= auth_t <= t + p):
            print('Ticket is expired')
            return None

        confirm_t = auth_t + 1
        encrypted_confirm_t = self.des.encrypt_data(confirm_t, key_ss_c)
        return encrypted_confirm_t


def init():
    kdc = KeyDistributionCenter()
    servers = [Server(sid, skey) for sid, skey in zip(kdc.available_servers, kdc.servers_keys)]
    client = Client(kdc.available_clients[0], kdc.clients_keys[0], kdc, servers)

    for idx, server in enumerate(servers):
        print(f'Server{idx} id: {server.server_id}, Server{idx} key: {server.server_key}')

    print(f'Client id: {client.client_id}, Client key: {client.client_key}')

    return client


def main():
    client = init()
    client.make_server_call(0)

if __name__ == "__main__":
    main()
