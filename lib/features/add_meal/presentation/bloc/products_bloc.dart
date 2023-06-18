import 'package:equatable/equatable.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:logging/logging.dart';
import 'package:opennutritracker/features/add_meal/domain/entity/product_entity.dart';
import 'package:opennutritracker/features/add_meal/domain/usecase/search_products_usecase.dart';

part 'products_event.dart';

part 'products_state.dart';

class ProductsBloc extends Bloc<ProductsEvent, ProductsState> {
  final log = Logger('ProductsBloc');

  final SearchProductsUseCase searchProductUseCase = SearchProductsUseCase();

  ProductsBloc() : super(ProductsInitial()) {
    on<LoadProductsEvent>((event, emit) async {
      emit(ProductsLoadingState());
      try {
        final result = await searchProductUseCase
            .searchOFFProductsByString(event.searchString);
        emit(ProductsLoadedState(products: result));
      } catch (error) {
        log.severe(error);
        emit(ProductsFailedState());
      }
    });
  }
}
