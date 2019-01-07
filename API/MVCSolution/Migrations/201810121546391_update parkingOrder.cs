namespace MVCSolution.Migrations
{
    using System;
    using System.Data.Entity.Migrations;
    
    public partial class updateparkingOrder : DbMigration
    {
        public override void Up()
        {
            DropPrimaryKey("dbo.ParkingOrders");
            AddColumn("dbo.ParkingOrders", "PowerOff", c => c.DateTime(nullable: false));
            AddColumn("dbo.ParkingOrders", "PowerOn", c => c.DateTime());
            AddColumn("dbo.ParkingOrders", "Price", c => c.Int(nullable: false));
            AddPrimaryKey("dbo.ParkingOrders", new[] { "DeviceId", "UserId", "PowerOff" });
            DropColumn("dbo.ParkingOrders", "AlarmOff");
            DropColumn("dbo.ParkingOrders", "AlarmOn");
        }
        
        public override void Down()
        {
            AddColumn("dbo.ParkingOrders", "AlarmOn", c => c.DateTime());
            AddColumn("dbo.ParkingOrders", "AlarmOff", c => c.DateTime());
            DropPrimaryKey("dbo.ParkingOrders");
            DropColumn("dbo.ParkingOrders", "Price");
            DropColumn("dbo.ParkingOrders", "PowerOn");
            DropColumn("dbo.ParkingOrders", "PowerOff");
            AddPrimaryKey("dbo.ParkingOrders", "DeviceId");
        }
    }
}
