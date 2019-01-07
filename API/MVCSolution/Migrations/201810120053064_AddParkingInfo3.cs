namespace MVCSolution.Migrations
{
    using System;
    using System.Data.Entity.Migrations;
    
    public partial class AddParkingInfo3 : DbMigration
    {
        public override void Up()
        {
            CreateTable(
                "dbo.ParkingOrders",
                c => new
                    {
                        DeviceId = c.String(nullable: false, maxLength: 128),
                        UserId = c.String(nullable: false, maxLength: 128),
                        AlarmOff = c.DateTime(nullable: true),
                        AlarmOn = c.DateTime(nullable: true),
                        Payed = c.Boolean(nullable: true),
                    })
                .PrimaryKey(t => t.DeviceId)
                .ForeignKey("dbo.AspNetUsers", t => t.UserId, cascadeDelete: true)
                .Index(t => t.UserId);
            
        }
        
        public override void Down()
        {
            DropForeignKey("dbo.ParkingOrders", "UserId", "dbo.AspNetUsers");
            DropIndex("dbo.ParkingOrders", new[] { "UserId" });
            DropTable("dbo.ParkingOrders");
        }
    }
}
