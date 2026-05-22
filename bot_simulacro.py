#!/usr/bin/env python3
"""
Bot Simulacro Bitcoin
Simula operaciones de trading en Bitcoin para fines educativos
"""

import json
import time
import random
from datetime import datetime
from typing import Dict, List, Optional

class BotSimulacroBitcoin:
    """Simulador de bot de trading en Bitcoin"""
    
    def __init__(self, saldo_inicial: float = 1000.0, config_file: str = "config.json"):
        """
        Inicializa el bot
        
        Args:
            saldo_inicial: Saldo inicial en USD
            config_file: Archivo de configuración
        """
        self.saldo_inicial = saldo_inicial
        self.saldo_actual = saldo_inicial
        self.btc_poseido = 0.0
        self.precio_btc_actual = random.uniform(40000, 70000)
        self.historial_transacciones: List[Dict] = []
        self.config = self._cargar_config(config_file)
        
    def _cargar_config(self, config_file: str) -> Dict:
        """Carga la configuración desde archivo"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "porcentaje_compra": 0.7,
                "porcentaje_venta": 1.3,
                "volatilidad": 0.02,
                "intervalo_actualización": 5
            }
    
    def simular_precio(self) -> float:
        """Simula la fluctuación del precio de Bitcoin"""
        volatilidad = self.config.get("volatilidad", 0.02)
        cambio = random.uniform(-volatilidad, volatilidad)
        self.precio_btc_actual *= (1 + cambio)
        return round(self.precio_btc_actual, 2)
    
    def comprar_bitcoin(self, cantidad_usd: float) -> bool:
        """
        Intenta comprar Bitcoin
        
        Args:
            cantidad_usd: Cantidad en USD a gastar
            
        Returns:
            True si la compra fue exitosa, False en caso contrario
        """
        if cantidad_usd > self.saldo_actual:
            print(f"❌ Saldo insuficiente. Disponible: ${self.saldo_actual:.2f}")
            return False
        
        btc_comprados = cantidad_usd / self.precio_btc_actual
        self.saldo_actual -= cantidad_usd
        self.btc_poseido += btc_comprados
        
        transaccion = {
            "tipo": "COMPRA",
            "timestamp": datetime.now().isoformat(),
            "cantidad_usd": cantidad_usd,
            "cantidad_btc": round(btc_comprados, 8),
            "precio_unitario": self.precio_btc_actual
        }
        self.historial_transacciones.append(transaccion)
        
        print(f"✅ Compra exitosa: {btc_comprados:.8f} BTC por ${cantidad_usd:.2f}")
        return True
    
    def vender_bitcoin(self, cantidad_btc: float) -> bool:
        """
        Intenta vender Bitcoin
        
        Args:
            cantidad_btc: Cantidad de Bitcoin a vender
            
        Returns:
            True si la venta fue exitosa, False en caso contrario
        """
        if cantidad_btc > self.btc_poseido:
            print(f"❌ No tienes suficientes Bitcoin. Disponible: {self.btc_poseido:.8f} BTC")
            return False
        
        cantidad_usd = cantidad_btc * self.precio_btc_actual
        self.btc_poseido -= cantidad_btc
        self.saldo_actual += cantidad_usd
        
        transaccion = {
            "tipo": "VENTA",
            "timestamp": datetime.now().isoformat(),
            "cantidad_btc": cantidad_btc,
            "cantidad_usd": round(cantidad_usd, 2),
            "precio_unitario": self.precio_btc_actual
        }
        self.historial_transacciones.append(transaccion)
        
        print(f"✅ Venta exitosa: {cantidad_btc:.8f} BTC por ${cantidad_usd:.2f}")
        return True
    
    def ejecutar_estrategia_automatica(self, ciclos: int = 10) -> None:
        """
        Ejecuta una estrategia automática de compra/venta
        
        Args:
            ciclos: Número de ciclos a ejecutar
        """
        print("🤖 Iniciando estrategia automática...")
        print(f"📊 Saldo inicial: ${self.saldo_inicial:.2f}\n")
        
        for i in range(ciclos):
            precio_anterior = self.precio_btc_actual
            nuevo_precio = self.simular_precio()
            cambio_porcentaje = ((nuevo_precio - precio_anterior) / precio_anterior) * 100
            
            print(f"Ciclo {i+1}/{ciclos}")
            print(f"  Precio BTC: ${nuevo_precio:.2f} ({cambio_porcentaje:+.2f}%)")
            print(f"  Tu balance: ${self.saldo_actual:.2f} | {self.btc_poseido:.8f} BTC")
            
            # Lógica simple de trading
            porcentaje_compra = self.config.get("porcentaje_compra", 0.7)
            porcentaje_venta = self.config.get("porcentaje_venta", 1.3)
            
            if cambio_porcentaje < -porcentaje_compra and self.saldo_actual > 100:
                # Compra si cae
                cantidad_compra = self.saldo_actual * 0.5
                self.comprar_bitcoin(cantidad_compra)
            
            elif cambio_porcentaje > porcentaje_venta and self.btc_poseido > 0:
                # Vende si sube
                cantidad_venta = self.btc_poseido * 0.5
                self.vender_bitcoin(cantidad_venta)
            
            print()
            time.sleep(self.config.get("intervalo_actualización", 5))
    
    def obtener_resumen(self) -> Dict:
        """Obtiene un resumen del estado actual del bot"""
        valor_btc = self.btc_poseido * self.precio_btc_actual
        valor_total = self.saldo_actual + valor_btc
        ganancia = valor_total - self.saldo_inicial
        porcentaje_ganancia = (ganancia / self.saldo_inicial) * 100
        
        return {
            "saldo_usd": round(self.saldo_actual, 2),
            "btc_poseido": round(self.btc_poseido, 8),
            "precio_btc": round(self.precio_btc_actual, 2),
            "valor_total": round(valor_total, 2),
            "ganancia": round(ganancia, 2),
            "porcentaje_ganancia": round(porcentaje_ganancia, 2),
            "total_transacciones": len(self.historial_transacciones)
        }
    
    def mostrar_resumen(self) -> None:
        """Muestra un resumen formateado"""
        resumen = self.obtener_resumen()
        
        print("\n" + "="*50)
        print("📊 RESUMEN FINAL DEL BOT")
        print("="*50)
        print(f"Saldo USD: ${resumen['saldo_usd']:.2f}")
        print(f"Bitcoin poseído: {resumen['btc_poseido']:.8f} BTC")
        print(f"Precio actual BTC: ${resumen['precio_btc']:.2f}")
        print(f"Valor total: ${resumen['valor_total']:.2f}")
        print(f"Ganancia: ${resumen['ganancia']:.2f} ({resumen['porcentaje_ganancia']:+.2f}%)")
        print(f"Total de transacciones: {resumen['total_transacciones']}")
        print("="*50 + "\n")


def main():
    """Función principal"""
    print("🚀 Bot Simulacro Bitcoin - Entra en el mejor momento\n")
    
    # Crear instancia del bot
    bot = BotSimulacroBitcoin(saldo_inicial=1000.0)
    
    # Ejecutar estrategia automática
    bot.ejecutar_estrategia_automatica(ciclos=10)
    
    # Mostrar resumen
    bot.mostrar_resumen()


if __name__ == "__main__":
    main()
