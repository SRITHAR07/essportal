import net.sf.jasperreports.engine.*;
import net.sf.jasperreports.engine.util.JRLoader;
import net.sf.jasperreports.view.JasperViewer;

import java.io.File;
import java.sql.Connection;
import java.sql.DriverManager;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

public class GenerateReport {
    private static final Logger LOGGER = Logger.getLogger(GenerateReport.class.getName());

    public static void main(String[] args) {
        String reportPath = "D:/gtn/reports/new.jasper"; // Path to compiled Jasper report
        String outputPdf = "D:/gtn/reports/generated_report.pdf";

        // ** Fix: Define Database Connection Variables **
        String url = "jdbc:sqlserver://localhost:1433;databaseName=emp;encrypt=false";
        String user = "sa";
        String password = "123";

        try (Connection connection = DriverManager.getConnection(url, user, password)) {
            LOGGER.info("Connected to the database successfully.");

            // ** Set parameters dynamically from args **
            Map<String, Object> parameters = new HashMap<>();
            parameters.put("Plantcode", args.length > 0 ? args[0] : "");
            parameters.put("Department", args.length > 1 ? args[1] : "");
            parameters.put("Designation", args.length > 2 ? args[2] : "");
            parameters.put("Subdepartment", args.length > 3 ? args[3] : "");
            parameters.put("Attendance", args.length > 4 ? args[4] : "");
            parameters.put("Gender", args.length > 5 ? args[5] : "");

            // ** Load and fill the report **
            File file = new File(reportPath);
            if (!file.exists()) {
                LOGGER.severe("Report file not found: " + reportPath);
                return;
            }

            JasperReport jasperReport = (JasperReport) JRLoader.loadObject(file);
            JasperPrint jasperPrint = JasperFillManager.fillReport(jasperReport, parameters, connection);

            // ** Export to PDF **
            JasperExportManager.exportReportToPdfFile(jasperPrint, outputPdf);
            LOGGER.info("Report generated successfully: " + outputPdf);

            // ** (Optional) Show Report Viewer **
            JasperViewer.viewReport(jasperPrint, false);
        } catch (Exception e) {
            LOGGER.log(Level.SEVERE, "Error generating report", e);
        }
    }
}


// java -cp ".;D:/gtn/reports/*" GenerateReport 
// javac -cp ".;D:/gtn/reports/*" GenerateReport.java
