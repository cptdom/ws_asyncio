from exchange.client import Client
import asyncio

SERVER = 'wss://currency-assignment.ematiq.com'
C = Client(SERVER)

def main():
    asyncio.run(C.run())