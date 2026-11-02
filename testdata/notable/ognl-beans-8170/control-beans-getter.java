public class BeanName {
    public static Object readName(Object bean) throws Exception {
        return new java.beans.Expression(bean, "getName", new Object[0]).getValue();
    }
}
