import javalang

code = '''
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
'''

tree = javalang.parse.parse(code)
print(tree.types[0].name)  # Output: Hello
