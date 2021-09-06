SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[loyalty_bucket](
	[id] [varchar](100) NOT NULL,
	[name] [varchar](100) NOT NULL,
	[created_at] [datetime] NULL,
	[updated_at] [datetime] NULL,
	[campaigns] [int] NULL,
	[customers] [int] NULL
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [dbo].[loyalty_bucket] ADD PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
