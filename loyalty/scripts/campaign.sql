SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[loyalty_campaign](
	[id] [varchar](100) NOT NULL,
	[name] [varchar](100) NOT NULL,
	[description] [text] NULL,
	[start_date] [datetime] NOT NULL,
	[end_date] [datetime] NOT NULL,
	[created_at] [datetime] NULL,
	[updated_at] [datetime] NULL,
	[bucket_id] [varchar](100) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [dbo].[loyalty_campaign] ADD PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [dbo].[loyalty_campaign]  WITH CHECK ADD FOREIGN KEY([bucket_id])
REFERENCES [dbo].[loyalty_bucket] ([id])
ON DELETE CASCADE
GO
