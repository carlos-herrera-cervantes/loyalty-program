SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[loyalty_customer](
	[id] [varchar](100) NOT NULL,
	[first_name] [varchar](100) NOT NULL,
	[last_name] [varchar](100) NOT NULL,
	[external_user_id] [varchar](100) NOT NULL,
	[birthdate] [date] NULL,
	[created_at] [datetime] NULL,
	[updated_at] [datetime] NULL,
	[bucket_id] [varchar](100) NULL
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [dbo].[loyalty_customer] ADD PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [dbo].[loyalty_customer]  WITH CHECK ADD FOREIGN KEY([bucket_id])
REFERENCES [dbo].[loyalty_bucket] ([id])
ON DELETE CASCADE
GO
