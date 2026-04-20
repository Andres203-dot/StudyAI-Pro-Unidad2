package com.smartlens.tcclosparcerosapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.runtime.Composable
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.smartlens.tcclosparcerosapp.data.SmartStockDatabase
import com.smartlens.tcclosparcerosapp.data.repository.StockRepository
import com.smartlens.tcclosparcerosapp.ui.product.ProductDetailScreen
import com.smartlens.tcclosparcerosapp.ui.product.ProductListScreen
import com.smartlens.tcclosparcerosapp.ui.product.ProductViewModel
import com.smartlens.tcclosparcerosapp.ui.stock.StockMovementScreen
import com.smartlens.tcclosparcerosapp.ui.theme.TCCLosparcerosAPPTheme

class MainActivity : ComponentActivity() {

    private val database by lazy { SmartStockDatabase.getDatabase(this) }
    private val repository by lazy { StockRepository(database.productDao(), database.stockMovementDao()) }
    private val viewModel: ProductViewModel by viewModels {
        ProductViewModel.Factory(repository)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            TCCLosparcerosAPPTheme {
                SmartStockApp(viewModel)
            }
        }
    }
}

@Composable
fun SmartStockApp(viewModel: ProductViewModel) {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = "product_list") {
        composable("product_list") {
            ProductListScreen(
                viewModel = viewModel,
                onProductClick = { productId ->
                    navController.navigate("stock_movements/$productId")
                },
                onAddProductClick = {
                    navController.navigate("product_detail/0")
                }
            )
        }
        composable(
            route = "product_detail/{productId}",
            arguments = listOf(navArgument("productId") { type = NavType.LongType })
        ) { backStackEntry ->
            val productId = backStackEntry.arguments?.getLong("productId")
            ProductDetailScreen(
                productId = if (productId == 0L) null else productId,
                viewModel = viewModel,
                onBack = { navController.popBackStack() }
            )
        }
        composable(
            route = "stock_movements/{productId}",
            arguments = listOf(navArgument("productId") { type = NavType.LongType })
        ) { backStackEntry ->
            val productId = backStackEntry.arguments?.getLong("productId") ?: 0L
            StockMovementScreen(
                productId = productId,
                viewModel = viewModel,
                onBack = { navController.popBackStack() }
            )
        }
    }
}
