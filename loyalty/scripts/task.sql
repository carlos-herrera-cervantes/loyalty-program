SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[loyalty_task](
	[id] [varchar](100) NOT NULL,
	[operator] [varchar](10) NOT NULL,
	[evaluationValue] [varchar](100) NULL,
	[evaluationValueType] [varchar](20) NULL,
	[comparisonValue] [varchar](100) NULL,
	[comparisonValueType] [varchar](20) NULL,
	[assignValue] [varchar](100) NULL,
	[assignValueType] [varchar](20) NULL,
	[customerProperty] [varchar](20) NULL,
	[type] [varchar](20) NOT NULL,
	[created_at] [datetime] NULL,
	[updated_at] [datetime] NULL,
	[event_code_id] [varchar](100) NOT NULL
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [dbo].[loyalty_task] ADD PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [dbo].[loyalty_task]  WITH CHECK ADD FOREIGN KEY([event_code_id])
REFERENCES [dbo].[loyalty_event_code] ([id])
ON DELETE CASCADE
GO
