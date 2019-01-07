namespace MVCSolution.Migrations
{
    using System;
    using System.Data.Entity.Migrations;
    
    public partial class AddParkingInfo4 : DbMigration
    {
        public override void Up()
        {
            AlterColumn("dbo.ParkingOrders", "AlarmOff", c => c.DateTime());
            AlterColumn("dbo.ParkingOrders", "AlarmOn", c => c.DateTime());
            AlterColumn("dbo.ParkingOrders", "Payed", c => c.Boolean());
        }
        
        public override void Down()
        {
            AlterColumn("dbo.ParkingOrders", "Payed", c => c.Boolean(nullable: false));
            AlterColumn("dbo.ParkingOrders", "AlarmOn", c => c.DateTime(nullable: false));
            AlterColumn("dbo.ParkingOrders", "AlarmOff", c => c.DateTime(nullable: false));
        }
    }
}
