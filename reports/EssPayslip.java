import net.sf.jasperreports.engine.*;
import net.sf.jasperreports.engine.export.HtmlExporter;
import net.sf.jasperreports.export.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.sql.*;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

public class EssPayslip {
    private static final Logger LOGGER = Logger.getLogger(EssPayslip.class.getName());

    public static void main(String[] args) {
        if (args.length < 2) {
            LOGGER.severe("Error: Missing required arguments (EmpID, Smonth).");
            return;
        }

        String empID = args[0].trim();
        String sMonth = args[1].trim();
        int empIDValue;

        try {
            empIDValue = Integer.parseInt(empID);
        } catch (NumberFormatException ex) {
            LOGGER.severe("Error: EmpID must be an integer.");
            return;
        }

        String dbUrl = "jdbc:sqlserver://localhost:1433;databaseName=emp;encrypt=false";
        String dbUsername = "sa";
        String dbPassword = "123";

        try (Connection connection = DriverManager.getConnection(dbUrl, dbUsername, dbPassword)) {
            LOGGER.info("Connected to SQL Server successfully!");

            // ✅ Load JRXML file dynamically and compile it
            String jrxmlFilePath = "D:/gtn/reports/epayslip.jrxml";
            if (!Files.exists(Paths.get(jrxmlFilePath))) {
                LOGGER.severe("Error: JRXML file not found at " + jrxmlFilePath);
                return;
            }

            JasperReport jasperReport = JasperCompileManager.compileReport(jrxmlFilePath);
            LOGGER.info("Compiled JRXML successfully!");

            // ✅ Set Parameters
            Map<String, Object> parameters = new HashMap<>();
            parameters.put("EmpID", empIDValue);
            parameters.put("Smonth", sMonth);

            // ✅ Fill the Jasper Report with Data
            JasperPrint jasperPrint = JasperFillManager.fillReport(jasperReport, parameters, connection);

            // ✅ Define Output Path
            String outputDir = "D:/gtn/reports/output/";
            String outputHtmlPath = outputDir + "generated_payslip.html";

            // Ensure Output Directory Exists
            Files.createDirectories(Paths.get(outputDir));

            // ✅ Export Report to HTML
            HtmlExporter htmlExporter = new HtmlExporter();
            htmlExporter.setExporterInput(new SimpleExporterInput(jasperPrint));
            htmlExporter.setExporterOutput(new SimpleHtmlExporterOutput(outputHtmlPath));

            // ✅ Configure HTML Export
            SimpleHtmlReportConfiguration reportConfig = new SimpleHtmlReportConfiguration();
            reportConfig.setWhitePageBackground(false);
            reportConfig.setRemoveEmptySpaceBetweenRows(true);

            SimpleHtmlExporterConfiguration exporterConfig = new SimpleHtmlExporterConfiguration();
            exporterConfig.setBetweenPagesHtml("<div style='page-break-before: always;'></div>");

            htmlExporter.setConfiguration(reportConfig);
            htmlExporter.setConfiguration(exporterConfig);
            htmlExporter.exportReport();

            LOGGER.info("Payslip report generated successfully at: " + outputHtmlPath);

        } catch (SQLException e) {
            LOGGER.log(Level.SEVERE, "Database connection error", e);
        } catch (JRException e) {
            LOGGER.log(Level.SEVERE, "JasperReports processing error", e);
        } catch (Exception e) {
            LOGGER.log(Level.SEVERE, "Unexpected error", e);
        }
    }
}
// java -cp ".;D:/gtn/reports/*" EssPayslip 
// javac -cp ".;D:/gtn/reports/*" EssPayslip.java
