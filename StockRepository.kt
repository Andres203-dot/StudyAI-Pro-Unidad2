package com.smartlens.tcclosparcerosapp.data.repository

import com.smartlens.tcclosparcerosapp.data.dao.ProductDao
import com.smartlens.tcclosparcerosapp.data.dao.StockMovementDao
import com.smartlens.tcclosparcerosapp.data.model.MovementType
import com.smartlens.tcclosparcerosapp.data.model.Product
import com.smartlens.tcclosparcerosapp.data.model.StockMovement
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.firstOrNull
import java.util.concurrent.TimeUnit

class StockRepository(
    private val productDao: ProductDao,
    private val stockMovementDao: StockMovementDao
) {
    val allProducts: Flow<List<Product>> = productDao.getAllProducts()
    val lowStockProducts: Flow<List<Product>> = productDao.getLowStockProducts()
    val allMovements: Flow<List<StockMovement>> = stockMovementDao.getAllMovements()

    fun getProductById(id: Long): Flow<Product?> = productDao.getProductById(id)

    suspend fun insertProduct(product: Product): Long = productDao.insertProduct(product)

    suspend fun updateProduct(product: Product) = productDao.updateProduct(product)

    suspend fun deleteProduct(product: Product) = productDao.deleteProduct(product)

    suspend fun addStockMovement(productId: Long, quantity: Int, reason: String? = null) {
        val type = if (quantity >= 0) MovementType.ENTRY else MovementType.EXIT
        val movement = StockMovement(
            productId = productId,
            quantity = quantity,
            type = type,
            reason = reason
        )
        
        // Insert movement
        stockMovementDao.insertMovement(movement)
        
        // Update product stock and recalculate prediction
        val product = productDao.getProductById(productId).firstOrNull()
        product?.let { p ->
            val newStock = p.currentStock + quantity
            
            // Recalculate average sales per day if it's an EXIT
            var newAvgSales = p.averageSalesPerDay
            if (type == MovementType.EXIT) {
                newAvgSales = calculateAverageSales(productId)
            }
            
            val updatedProduct = p.copy(
                currentStock = newStock,
                averageSalesPerDay = newAvgSales
            )
            productDao.updateProduct(updatedProduct)
        }
    }

    private suspend fun calculateAverageSales(productId: Long): Double {
        val movements = stockMovementDao.getMovementsByProduct(productId).first()
        val exits = movements.filter { it.type == MovementType.EXIT }
        
        if (exits.isEmpty()) return 0.0
        
        val firstExitTimestamp = exits.minByOrNull { it.timestamp }?.timestamp ?: return 0.0
        val totalExitQuantity = exits.sumOf { Math.abs(it.quantity) }
        
        val currentTime = System.currentTimeMillis()
        val diffInMillis = currentTime - firstExitTimestamp
        val diffInDays = TimeUnit.MILLISECONDS.toDays(diffInMillis).toDouble()
        
        // Avoid division by zero, if less than a day, treat as 1 day for initial calculation
        val days = if (diffInDays < 1.0) 1.0 else diffInDays
        
        return totalExitQuantity / days
    }

    fun getMovementsByProduct(productId: Long): Flow<List<StockMovement>> =
        stockMovementDao.getMovementsByProduct(productId)
}
