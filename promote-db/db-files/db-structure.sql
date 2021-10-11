CREATE DATABASE [PromoteDB]
GO

USE [PromoteDB]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Radoslav Ganov
-- Create date: 2012-12-10
-- Description:	Create a new Execution
-- =============================================
CREATE PROCEDURE [dbo].[CreateExecution] 
AS
BEGIN
  SET NOCOUNT ON;
  DECLARE @ExecutionDate datetime2(7) = GETDATE()
                                            
  INSERT INTO PromotedExecution (ExecutionDate, ExecutedBy)
  VALUES (@ExecutionDate,SYSTEM_USER)
  SELECT IDENT_CURRENT('PromotedExecution') AS ExecutionID, @ExecutionDate AS ExecutionDate
END
                                                                       
                                            
GO
/****** Object:  StoredProcedure [dbo].[ProcessFile]  ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Radoslav Ganov
-- Create date: 2012-12-20
-- Description:	Set fiel process status
-- =============================================
CREATE PROCEDURE [dbo].[ProcessFile] 
  @ExecutionId int,
  @FullFileName nvarchar(260),
  @FileProcessedSuccessfully int = 0,
  @ErrorMessage nvarchar(260)
AS
BEGIN
                                            
  SET NOCOUNT ON;
                                            
  IF @FileProcessedSuccessfully = 1 
    BEGIN
    UPDATE [dbo].[PromotedExecutionInventory]
    SET [Status] = 1
    WHERE ExecutionId = @ExecutionId
      AND FullFileName = @FullFileName
      
    END
  ELSE
    BEGIN

    UPDATE [dbo].[PromotedExecutionInventory]
    SET [Status] = 2, [ErrorMessage] = @ErrorMessage
    WHERE ExecutionId = @ExecutionId
      AND FullFileName = @FullFileName

    UPDATE [dbo].[PromotedExecution]
    SET [ErrorOnFile] = @FullFileName
    WHERE [ExecutionID] = @ExecutionId
                                      
    END
END

GO
/****** Object:  StoredProcedure [dbo].[GetFiles]    ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Radoslav Ganov
-- Create date: 2012-12-09
-- Description:	get delta between processed and new files
-- =============================================
CREATE PROCEDURE [dbo].[GetFiles]
@ExecutionId int
AS
BEGIN
                                            	
  SELECT pei.[FullFileName], pei.[ConnectionManager]
  FROM [PromoteDB].[dbo].[PromotedExecutionInventory] pei
  WHERE pei.ExecutionID = @ExecutionId
                                            	
  RETURN 
END
                                            
GO
/****** Object:  StoredProcedure [dbo].[FinishExecution]    ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Radoslav Ganov
-- Create date: 2012-12-09
-- Description: 
-- =============================================
CREATE PROCEDURE [dbo].[FinishExecution]
@ExecutionId int,
@FileCount int
AS
BEGIN
                                            	
  UPDATE [dbo].[PromotedExecution] 
  SET [FilesProcessed] = @FileCount 
  WHERE [ExecutionID] = @ExecutionId
                                            	
  RETURN 
END
                                            
GO
/****** Object:  StoredProcedure [dbo].[InsertFilesToProcess]    ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Radoslav Ganov
-- Create date: 2012-12-09
-- Description:	
-- =============================================
CREATE PROCEDURE [dbo].[InsertFilesToProcess]
@ExecutionId int,
@ExecutionDate datetime2(7),
@FullFileName nvarchar(260),
@ConnectionManager nvarchar(255)
AS
BEGIN
                                            	
  INSERT INTO [dbo].[PromotedExecutionInventory]
  (
    [FullFileName],
    [ConnectionManager],
    [ExecutionID],
    [ExecutedBy],
    [ExecutionDate]
  )
  VALUES
  (
    @FullFileName,
    @ConnectionManager,
    @ExecutionId,
    SYSTEM_USER,
    @ExecutionDate
  );
                                            	
  RETURN 
END
                                            
GO
/****** Object:  Table [dbo].[PromotedExecution]    ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[PromotedExecution](
  [ExecutionID] [int] IDENTITY(1,1) NOT NULL,
  [ExecutedBy] [nvarchar](50) NOT NULL,
  [ExecutionDate] [datetime2](7) NOT NULL,
  [FilesProcessed] [int] NULL,
  [ErrorOnFile] [nvarchar](260) NULL,
  CONSTRAINT [PK_PromotedExecution] PRIMARY KEY CLUSTERED 
(
  [ExecutionID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
                                            
GO
/****** Object:  Table [dbo].[PromotedExecutionInventory]    ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[PromotedExecutionInventory](
  [ExecutionDate] [datetime2](7) NOT NULL,
  [ExecutionID] [int] NOT NULL,
  [FullFileName] [nvarchar](260) NOT NULL,
  [ConnectionManager] [nvarchar](255) NOT NULL,
  [Status] [int] NULL,
  [ErrorMessage] [nvarchar](255) NULL,
  [ExecutedBy] [nvarchar](50) NOT NULL,
  CONSTRAINT [PK_PromotedExecutionInventory] PRIMARY KEY CLUSTERED 
(
  [ExecutionID], [ExecutionDate]
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]                           
                                          
GO
ALTER TABLE [dbo].[PromotedExecutionInventory] ADD  DEFAULT ((0)) FOR [Status]
GO