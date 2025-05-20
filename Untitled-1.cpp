#include <iostream>

int main() {
    int num1, num2, result;

    std::cout << "Enter two numbers: ";
    std::cin >> num1 >> num2;

    result = num1 * num2;

    std::cout << "The result of multiplication is: " << result << std::endl;

    return 0;
}