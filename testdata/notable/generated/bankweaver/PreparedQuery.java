class SearchService implements JavaService2 {
 Object invoke(DataControllerRequest req) throws Exception {
   String key = req.getParameter("sql");
   Connection db = DriverManager.getConnection("jdbc:postgresql://db.invalid/demo", "app", "");
   PreparedStatement st = db.prepareStatement("SELECT id FROM items WHERE id = ?");
   st.setString(1, key);
   return st.executeQuery();
 }
}
