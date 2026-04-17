import java.util.logging.Logger;

final class Sample {
    private static final Logger LOGGER = Logger.getLogger(Sample.class.getName());

    private Sample() {}

    public static void main(String[] args) {
        LOGGER.info("this sample does nothing");
    }
}
