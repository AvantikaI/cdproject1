class error{

    public static void main(String[] args) {

        // 1. Missing semicolon
        int x = 10

        // 2. Unused variable
        int unusedVariable = 100;

        // 3. Undeclared variable
        int y = undeclaredVar + 5;

        // 4. Type mismatch
        String z = 50;

        // 5. Missing brackets
        if (x > 5)
            System.out.println("X is greater than 5");

        // 6. Hardcoded password
        String password = "mySecret123";

        // 7. SQL Injection risk
        String userInput = "admin";
        String query = "SELECT * FROM users WHERE name = '" + userInput + "'";
        statement.executeQuery(query);

        // 8. Undefined method call
        callThisDoesNotExist();

    // <-- 9. Missing closing brace for main method and class