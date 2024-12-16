class Car {
  // Public properties
  String brand;
  String model;
  int year;

  // Constructor
  Car(this.brand, this.model, this.year);

  // Method to calculate the car's age
  int carAge() {
    int currentYear = DateTime.now().year;
    return currentYear - year;
  }
}

void main() {
  // Creating an instance of Car
  Car myCar = Car('Toyota', 'Corolla', 2015);

  // Displaying the car's information
  print('Brand: ${myCar.brand}');
  print('Model: ${myCar.model}');
  print('Year: ${myCar.year}');
  print('Car Age: ${myCar.carAge()} years');
}
