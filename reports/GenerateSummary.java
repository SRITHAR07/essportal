import net.sf.jasperreports.engine.*;
import java.sql.*;
import java.util.HashMap;
import java.util.Map;
import net.sf.jasperreports.engine.export.HtmlExporter;
import net.sf.jasperreports.export.SimpleExporterInput;
import net.sf.jasperreports.export.SimpleHtmlExporterOutput;
import net.sf.jasperreports.export.SimpleHtmlReportConfiguration;
import net.sf.jasperreports.export.SimpleHtmlExporterConfiguration;
import java.io.File;

public class GenerateSummary {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Error: Missing required argument (GroupBy: Deptname, Subdeptname, or Designame).");
            return;
        }

        String groupBy = args[0].trim(); // Accept dynamic grouping

        try {
            // Step 1: Connect to SQL Server
            String dbUrl = "jdbc:sqlserver://localhost:1433;databaseName=emp;encrypt=false";
            String dbUsername = "sa";
            String dbPassword = "123";
            Connection connection = DriverManager.getConnection(dbUrl, dbUsername, dbPassword);
            System.out.println("Connected to SQL Server successfully!");

            // Step 2: Compile JRXML to JasperReport
            String jrxmlFilePath = "D:/gtn/reports/summary.jrxml"; // Your existing JRXML file
            JasperReport jasperReport = JasperCompileManager.compileReport(jrxmlFilePath);

            // Step 3: Set Parameters (only for grouping)
            Map<String, Object> parameters = new HashMap<>();
            parameters.put("group_by", groupBy);

            // Step 4: Query with Dynamic Grouping
            String query = "WITH GroupedData AS (" +
                           "    SELECT " +
                           "        CASE " +
                           "            WHEN ? = 'Deptname' THEN d.Deptname " +
                           "            WHEN ? = 'Subdeptname' THEN s.Subdeptname " +
                           "            WHEN ? = 'Designame' THEN g.Designame " +
                           "        END AS GroupField, " +
                           "        e.Gender, t.Attn " +
                           "    FROM dbo.Mas_Emp_Official e " +
                           "    INNER JOIN dbo.app_temp_attn t ON e.ID = t.EmpID " +
                           "    LEFT JOIN dbo.Mas_Dept d ON e.DeptID = d.ID " +
                           "    LEFT JOIN dbo.Mas_Subdept s ON e.SubdeptID = s.ID " +
                           "    LEFT JOIN dbo.Mas_Designation g ON e.Desigid = g.ID " +
                           ") " +
                           "SELECT " +
                           "    GroupField, " +
                           "    COUNT(CASE WHEN Gender = 'Male' AND Attn = 'P' THEN 1 END) AS Male_Present, " +
                           "    COUNT(CASE WHEN Gender = 'Male' AND Attn = 'AB' THEN 1 END) AS Male_Absent, " +
                           "    COUNT(CASE WHEN Gender = 'Female' AND Attn = 'P' THEN 1 END) AS Female_Present, " +
                           "    COUNT(CASE WHEN Gender = 'Female' AND Attn = 'AB' THEN 1 END) AS Female_Absent " +
                           "FROM GroupedData " +
                           "GROUP BY GroupField " +
                           "ORDER BY GroupField;";

            PreparedStatement statement = connection.prepareStatement(query);
            statement.setString(1, groupBy);
            statement.setString(2, groupBy);
            statement.setString(3, groupBy);

            ResultSet resultSet = statement.executeQuery();
            JRResultSetDataSource dataSource = new JRResultSetDataSource(resultSet);

            // Step 5: Fill the Jasper Report with Data
            JasperPrint jasperPrint = JasperFillManager.fillReport(jasperReport, parameters, dataSource);

            // Step 6: Export Report to HTML with Page Breaks
            String outputHtmlPath = "D:/gtn/reports/output/generated_report.html";

            // ✅ Use HtmlExporter (New API)
            HtmlExporter htmlExporter = new HtmlExporter();
            htmlExporter.setExporterInput(new SimpleExporterInput(jasperPrint));

            // ✅ Define Export Output
            SimpleHtmlExporterOutput exporterOutput = new SimpleHtmlExporterOutput(outputHtmlPath, "UTF-8");
            htmlExporter.setExporterOutput(exporterOutput);


            // ✅ Add Page Breaks in HTML
            SimpleHtmlExporterConfiguration exporterConfig = new SimpleHtmlExporterConfiguration();
            exporterConfig.setBetweenPagesHtml("<div style='page-break-before: always;'></div>");
            
            // ✅ Export Report
            htmlExporter.exportReport();

            System.out.println("Grouped report generated successfully with page breaks in HTML format!");

        } catch (Exception e) {
            System.out.println("Error generating report:");
            e.printStackTrace();
        }
    }
}


// java -cp ".;D:/gtn/reports/*" GenerateSummary 
// javac -cp ".;D:/gtn/reports/*" GenerateSummary.java
