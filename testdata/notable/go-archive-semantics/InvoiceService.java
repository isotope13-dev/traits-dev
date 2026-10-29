package pl.hackerspace.service;

import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.InputStreamResource;
import org.springframework.core.io.Resource;
import org.springframework.http.ContentDisposition;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StreamUtils;
import pl.hackerspace.domain.Client;
import pl.hackerspace.domain.Invoice;
import pl.hackerspace.dto.CustomInvoiceDataDto;
import pl.hackerspace.dto.InvoiceGenerationDto;
import pl.hackerspace.repository.ClientRepository;
import pl.hackerspace.repository.InvoiceRepository;

import java.io.BufferedInputStream;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import static pl.hackerspace.service.TemplateService.withTemplate;

@Slf4j
@Service
@RequiredArgsConstructor
public class InvoiceService {

    private final ClientRepository clientRepository;

    private final InvoiceRepository invoiceRepository;

    @Transactional
    public ResponseEntity<Resource> generateNewInvoice(InvoiceGenerationDto generationRequest) throws IOException {
        Client client = clientRepository.findById(generationRequest.getNip()).orElseThrow(() -> new RuntimeException("Not found"));
        return withTemplate(template -> {
            byte[] invoice;
            if (!client.isSubscriber() || generationRequest.getCustomInvoiceData() != null) {
                invoice = createPdfInvoice(client, template, null, generationRequest.getCustomInvoiceData());
            } else {
                invoice = getOrCreateSubscriptionPdfInvoice(template, client, generationRequest.getMonthOfInvoice());
            }
            return ResponseEntity.ok()
                    .headers(getHttpHeaders(client.getName() + " " + generationRequest.getMonthOfInvoice()))
                    .contentLength(-1)
                    .contentType(MediaType.APPLICATION_PDF)
                    .body(new ByteArrayResource(invoice));
        });
    }


    @Transactional
    public void generateInvoicesForAllSubscribers(HttpServletResponse response, String monthOfInvoice) throws IOException {
        setHeaders(response, "application/zip", LocalDate.now().format(DateTimeFormatter.ISO_LOCAL_DATE) + ".zip");
        List<Client> subscribers = clientRepository.findBySubscriberTrue();
        withTemplate(template -> {
            try (ZipOutputStream zipOutputStream = new ZipOutputStream(response.getOutputStream())) {
                for (Client client : subscribers) {
                    try (InputStream inputStream = new ByteArrayInputStream(
                            getOrCreateSubscriptionPdfInvoice(template, client, monthOfInvoice))) {
                        zipOutputStream.putNextEntry(new ZipEntry(getPdfFilename(client.getName() + " "
                                + monthOfInvoice)));
                        StreamUtils.copy(inputStream, zipOutputStream);
                        zipOutputStream.flush();
                    }
                }
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            return null;
        });
    }

    private byte[] getOrCreateSubscriptionPdfInvoice(String template, Client client, final String monthOfInvoice) {
        byte[] invoice = client.getInvoiceForSubscriptionMonth(monthOfInvoice);
        if (invoice == null) {
            invoice = createPdfInvoice(client, template, monthOfInvoice, null);
        }
        return invoice;
    }

    private static void setHeaders(HttpServletResponse response, String contentType, String filename) {
        response.setContentType(contentType);
        response.setHeader(HttpHeaders.CONTENT_DISPOSITION, ContentDisposition.attachment()
                .filename(filename, StandardCharsets.UTF_8)
                .build()
                .toString());
    }

    private byte[] createPdfInvoice(Client client, String template, String monthOfSubscription,
                                    CustomInvoiceDataDto customInvoiceData) {
        LocalDateTime creationDate = LocalDateTime.now();
        Invoice newInvoice = createNewInvoice(client, creationDate, monthOfSubscription);
        byte[] bytes = TemplateService.convertHtmlToPdf(template, client, creationDate,
                newInvoice.getInvoiceTitle(), monthOfSubscription, customInvoiceData);
        newInvoice.setPdfContent(bytes);
        save(newInvoice);
        return bytes;
    }

    private static HttpHeaders getHttpHeaders(final String filename) {
        HttpHeaders headers = new HttpHeaders();
        headers.add(HttpHeaders.ACCESS_CONTROL_EXPOSE_HEADERS, HttpHeaders.CONTENT_DISPOSITION);
        headers.add(HttpHeaders.CONTENT_TYPE, "application/octet-stream");
        headers.add(HttpHeaders.CONTENT_DISPOSITION, "inline; filename=" + getPdfFilename(filename));
        return headers;
    }

    private static String getPdfFilename(String filename) {
        return filename + ".pdf";
    }

    public Invoice createNewInvoice(Client client, final LocalDateTime creationDate, String monthOfSubscription) {
        long nextInvoiceId = invoiceRepository.getMaxId() + 1;
        return Invoice.builder().id(nextInvoiceId)
                .invoiceTitle("FV" + nextInvoiceId)
                .creationDate(creationDate)
                .monthOfSubscription(monthOfSubscription)
                .client(client)
                .build();
    }

    public void save(Invoice newInvoice) {
        invoiceRepository.save(newInvoice);
    }

    public List<Invoice> findAll() {
        return invoiceRepository.findAll();
    }
}
